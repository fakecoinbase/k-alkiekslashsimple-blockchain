import collections

from util.helpers import hash_transaction, verify_signature, sign


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
            'value': self.__value,
            'recipient_pk': self.__payee_pk
        })

    def to_dict(self):
        return self.__to_dict()

    def sign(self, sk):
        self.__signature = sign(str(self.__to_dict()), sk)

    def verify(self):
        return verify_signature(self.__payee_pk, self.__signature, str(self.__to_dict()))

    def get_signature(self):
        return self.__signature
