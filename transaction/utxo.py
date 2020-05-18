import collections

from cryptography.exceptions import InvalidSignature

from util.helpers import hash_transaction
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class Utxo:

    def __init__(self, tx, op_index):
        self.__payee_pk = tx.destinations[op_index - 1][0]
        self.__tx_hash = hash_transaction(tx)
        self.__idx = op_index
        self.__value = tx.destinations[op_index - 1][1]
        self.__signature = b''

    def get_value(self):
        return self.__value

    def get_recipient_pk(self):
        return self.__payee_pk

    def get_transaction_hash(self):
        return self.__tx_hash

    def get_index(self):
        return self.__idx

    def __to_dict(self):
        return collections.OrderedDict({
            'tx_hash': self.__tx_hash,
            'index': self.__idx,
            'value': self.__value
        })

    def sign(self, sk):
        self.__signature = sk.sign(
            data=str(self.__to_dict()).encode('utf-8'),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hashes.SHA256()
        )

    def verify(self):
        try:
            self.__payee_pk.verify(
                signature=self.__signature,
                data=str(self.__to_dict()).encode('utf-8'),
                padding=padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                algorithm=hashes.SHA256()
            )
        except InvalidSignature:
            print("Invalid Signature")
            return False
        return True
