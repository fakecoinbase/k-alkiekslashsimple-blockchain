from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from chain.blockchain import Blockchain
from util.helpers import verify_signature

CHAIN_SIZE = 200


class Miner:
    def __init__(self):
        self.__secret_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1028,
            backend=default_backend()
        )
        self.public_key = self.__secret_key.public_key()
        self.__blockchain = Blockchain(CHAIN_SIZE)
        self.__unconfirmed_tx_pool = []

    def verify_block(self, block):
        return True

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


