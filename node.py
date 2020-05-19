from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from chain.block import Block
from chain.blockchain import Blockchain
from util.helpers import  DIFFICULTY_LEVEL, BASE_VALUE
from transaction.transaction import Transaction
import random


class Client:

    def __init__(self, mode='POW'):
        self.mining_mode = mode
        self.__secret_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1028,
            backend=default_backend()
        )
        self.public_key = self.__secret_key.public_key()
        self.__wallet = []
        self.__blockchain = None
        self.genesis_block()

    # TODO: Change the hardcoded pk with the actual models pk
    def genesis_block(self):
        transactions = []
        for i in range(1, 51):
            transactions.append(Transaction(outputs=[(i, BASE_VALUE)]))
        genesis_block = Block(transactions=transactions, previous_hash="genesis")
        self.__blockchain = Blockchain(block=genesis_block)
        self.__wallet.append(transactions[0].get_outputs()[0])

    # TODO: delete this method after integration
    def get_sk(self):
        return self.__secret_key

    # TODO: transaction generation mechanism
    def generate_tx(self, outputs, prev_tx_hash, output_index):
        for utxo in self.__wallet:
            if utxo.get_transaction_hash() == prev_tx_hash and utxo.get_index() == output_index:
                utxo.sign(self.__secret_key)
                tx = Transaction(originator_sk=self.__secret_key, originator_pk=self.public_key, inputs=[utxo],
                                 outputs=outputs, witnesses_included=True)
                tx.sign_transaction()
                return tx

    def maybe_store_output(self, block):
        for tx in block.transactions():
            for op in tx.get_outputs():
                if op.get_recipient_pk() == self.public_key:
                    self.__wallet.append(op)

    def verify_block(self, block):
        # Step #1
        # check the difficulty number of zeros in the block hash
        if self.mining_mode == 'POW':
            if block.hash_difficulty() != DIFFICULTY_LEVEL:
                return False

        # Step #2:
        # check the referenced previous block
        return self.__blockchain.add_block(block)

    # TODO: delete this method after integration
    def get_random_input(self):
        return random.choice(self.__wallet)

    # TODO: delete this method after integration
    def wallet_size(self):
        return len(self.__wallet)