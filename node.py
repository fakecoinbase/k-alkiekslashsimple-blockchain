from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from chain.blockchain import Blockchain
from miner import CHAIN_SIZE, DIFFICULTY_LEVEL
from transaction.transaction import Transaction


class Client:

    def __init__(self):
        self.__secret_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1028,
            backend=default_backend()
        )
        self.public_key = self.__secret_key.public_key()
        self.__wallet = []
        self.__blockchain = Blockchain(CHAIN_SIZE)  # there should be the genesis block

    # TODO: delete this method after integration
    def get_sk(self):
        return self.__secret_key

    # TODO: transaction generation mechanism
    def generate_tx(self, outputs, prev_tx_hash, output_index):
        for utxo in self.__wallet:
            if utxo.get_transaction_hash() == prev_tx_hash and utxo.get_index() == output_index:
                utxo.sign()
                tx = Transaction(self.__secret_key, self.public_key, utxo, outputs, True)
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