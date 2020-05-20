import random
from typing import List

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from chain.block import Block
from chain.blockchain import Blockchain
from client.broadcast_event import BroadcastEvent
from miningThread import MiningThread
from model._bft.bft_context import BFTContext
from model._bft.bft_state import PrePreparedState
from model._broadcast_handler import BroadcastHandler
from model._server_handler import ServerHandler
from transaction.transaction import Transaction
from transaction.utxo import Utxo
from util.helpers import BASE_VALUE, DIFFICULTY_LEVEL, verify_signature, hash_transaction, sign, CHAIN_SIZE
from util.message.bft import PrePrepareMessage, PrepareMessage, CommitMessage
from util.peer_data import PeerData


class Model:
    active_peers: List[PeerData]
    peer_data: PeerData
    server_handler: ServerHandler
    broadcast_handler: BroadcastHandler
    bft_context: BFTContext
    peers_database: List[PeerData]

    def __init__(self, peer_data, sk, server_queue, broadcast_queue, peers_database, mode, bft_leader=False,
                 mining_mode='pow'):
        self.mining_mode = mining_mode
        self.peers_database = peers_database
        self.peer_data = peer_data
        self.server_queue = server_queue
        self.broadcast_queue = broadcast_queue
        self.active_peers = []
        self.server_handler = ServerHandler(self)
        self.broadcast_handler = BroadcastHandler(self)
        self.bft_context = BFTContext(self.active_peers, self, bft_leader)
        if mode == 'client':
            self.sk = sk
            self.pk = serialization.load_pem_public_key(peer_data.pk, backend=default_backend())
            self.__wallet = []
        elif mode == 'miner':
            self.unconfirmed_tx_pool = []
            self.__mining_thread = None
        self.blockchain = None
        self.mode = mode
        self.genesis_block()

    def handle_broadcast_responses(self, message, responses):
        return self.broadcast_handler.handle(message, responses)

    def handle_server_message(self, message):
        return self.server_handler.handle(message)

    def broadcast_pre_prepare(self, message: PrePrepareMessage):
        self.bft_context.transition_to(PrePreparedState)
        self.bft_context.pre_prepare_message = message
        pre_prepare_event = BroadcastEvent(message)
        with pre_prepare_event.condition:
            self.broadcast_queue.put(pre_prepare_event)
            pre_prepare_event.condition.wait()
        print(pre_prepare_event.responses)

    def broadcast_prepare(self, message: PrepareMessage):
        prepare_event = BroadcastEvent(message)
        self.broadcast_queue.put(prepare_event)

    def broadcast_commit(self, message: CommitMessage):
        commit_event = BroadcastEvent(message)
        self.broadcast_queue.put(commit_event)

    # TODO: Change the hardcoded pk with the actual models pk Test
    # Miner and Client
    def genesis_block(self):
        transactions = []
        for peer in self.peers_database:
            if peer.pk is not None:
                transactions.append(Transaction(outputs=[(peer.pk, BASE_VALUE)]))

        if self.mode == 'client':
            self.__wallet.append(Transaction(outputs=[(self.peer_data.pk, BASE_VALUE)]).get_outputs()[0])
        genesis_block = Block(transactions=transactions, previous_hash="genesis", height=0)
        self.blockchain = Blockchain(block=genesis_block)

    # TODO: transaction generation mechanism
    # Client
    def generate_tx(self, outputs, utxo):
        utxo.sign(self.sk)
        tx = Transaction(peer_data=self.peer_data, inputs=[utxo],
                         outputs=outputs, witnesses_included=True)
        msg = str(tx.to_dict())
        signature = sign(msg, self.sk)
        tx.sign_transaction(signature)
        return tx

    # TODO: delete this method after integration
    # Client
    def get_random_input(self) -> Utxo:
        return random.choice(self.__wallet)

    # Client
    def get_wallet(self):
        return self.__wallet

    # Miner
    def maybe_store_output(self, block):
        for tx in block.transactions():
            for op in tx.get_outputs():
                if op.get_recipient_pk() == self.pk:
                    self.__wallet.append(op)

    # Miner and Client
    def verify_block(self, block):
        if self.mode == 'miner':
            if self.__mining_thread.is_alive():
                self.__mining_thread.stop()
                self.__mining_thread.join()
                self.unconfirmed_tx_pool.remove(block.transactions)
        # Step #1
        # check the difficulty number of zeros in the block hash
        if self.mining_mode == 'pow':
            if block.hash_difficulty() != DIFFICULTY_LEVEL:
                return False

        # Step #2:
        # check the referenced previous block
        result = self.blockchain.add_block(block)
        # if result:
        # TODO: broadcast block

    # Miner
    def add_transaction(self, tx):
        if self.validate_transaction(tx):
            self.unconfirmed_tx_pool.append(tx)

        if len(self.unconfirmed_tx_pool) >= CHAIN_SIZE and (self.__mining_thread is None or not self.is_mining()):
            self.__mining_thread = MiningThread(self)
            self.__mining_thread.start()
        #     self.__mining_thread.set_data(self.unconfirmed_tx_pool[0: CHAIN_SIZE],
        #                                   self.blockchain.get_head_of_chain().block.block_hash, DIFFICULTY_LEVEL)
        #     self.__mining_thread.start()
        #     self.__mining_thread.join()     # TODO: don't wait for pow
        #     self.unconfirmed_tx_pool[0:CHAIN_SIZE] = []
        #     self.verify_block(self.__mining_thread.get_block())

    # Miner
    def validate_transaction(self, tx):
        # Step #1:
        # make sure that the originator is the actual recipient of the input utxos
        signature = tx.get_signature()
        public_key = tx.get_peer_data().pk
        tx_original = tx
        tx = tx.to_dict()
        used_value = 0
        for ip in tx['inputs']:
            used_value += ip.get_value()
            if not ip.verify():
                print("Invalid input.")
                return False
        # Step #2:
        # check overspending
        transferred_value = 0
        for op in tx['outputs']:
            if op.get_recipient_pk() != public_key:
                transferred_value += op.get_value()
        if transferred_value > used_value:
            print("Overspending rejected.")
            return False
        # Step #3:
        # check double spending
        # TODO:Double spending Test
        if self.blockchain.get_block_of_transaction(hash_transaction(tx_original)) is not None:
            print("Double Spending rejected.")
            return False
        return True

    # Miner
    def is_mining(self):
        return self.__mining_thread.is_alive()
