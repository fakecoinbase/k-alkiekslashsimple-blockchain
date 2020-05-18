from util.helpers import hash_transaction


class Utxo:

    def __init__(self, tx, op_index):
        self.__payee_pk = tx.destinations[op_index - 1][0]
        self.__tx_hash = hash_transaction(tx)
        self.__idx = op_index
        self.__value = tx.destinations[op_index - 1][1]

    def get_value(self):
        return self.__value

    def get_recipient_pk(self):
        return self.__payee_pk

    def get_transaction_hash(self):
        return self.__tx_hash

    def get_index(self):
        return self.__idx
