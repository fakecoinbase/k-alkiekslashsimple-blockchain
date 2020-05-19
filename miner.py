from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from chain.block import Block
from chain.blockchain import Blockchain
from miningThread import MiningThread
from transaction.transaction import Transaction
from util.helpers import verify_signature

CHAIN_SIZE = 200
DIFFICULTY_LEVEL = 3


class Miner:
    def __init__(self, mode='POW'):
        self.__secret_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1028,
            backend=default_backend()
        )
        self.mining_mode = mode
        self.public_key = self.__secret_key.public_key()
        genesis_block = Block(previous_hash="genesis")
        self.__blockchain = None
        genesis_block()
        self.__unconfirmed_tx_pool = []
        self.__mining_thread = MiningThread()

    # TODO: delete this method after integration
    def genesis_block(self):
        transactions = []
        for i in range(1, 51):
            transactions.append((i, 5))
        genesis_block = Block(transactions=transactions, previous_hash="genesis")
        self.__blockchain = Blockchain(block=genesis_block)

    def verify_block(self, block):
        if self.__mining_thread.is_alive():
            self.__mining_thread.stop()
            self.__mining_thread.join()
            self.__unconfirmed_tx_pool.remove(block.transactions)

        # Step #1
        # check the difficulty number of zeros in the block hash
        if self.mining_mode == 'POW':
            if block.hash_difficulty() != DIFFICULTY_LEVEL:
                return False

        # Step #2:
        # check the referenced previous block
        return self.__blockchain.add_block(block)

    def add_transaction(self, tx):
        if self.validate_transaction(tx):
            self.__unconfirmed_tx_pool.append(tx)
        if len(self.__unconfirmed_tx_pool) >= CHAIN_SIZE:
            self.__mining_thread.set_data(self.__unconfirmed_tx_pool[0: 50],
                                          self.__blockchain.get_head_of_chain().block.block_hash(), DIFFICULTY_LEVEL)
            self.__mining_thread.start()
            self.__unconfirmed_tx_pool[0:50] = []
            self.verify_block(self.__mining_thread.get_block())

    def validate_transaction(self, tx):
        # Step #1:
        # make sure that the originator is the actual recipient of the input utxos
        signature = tx.get_signature()
        tx = tx.to_dict()
        public_key = tx['originator']
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
        # validate the signature of the originator
        return verify_signature(public_key, signature, str(tx))
        # Step #4:
        # check double spending
        # TODO:Double spending
