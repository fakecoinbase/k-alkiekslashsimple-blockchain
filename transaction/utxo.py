from hashlib import sha256


class Utxo:

    def __init__(self, tx, op_index, value, pk):
        self.tx_signature = tx.get_signature()
        self.__payee_pk = pk
        self.__tx_hash = sha256(str(tx.to_dict()).encode('utf-8')).hexdigest()
        self.__idx = op_index
        self.__value = value

    def get_value(self):
        return self.__value

    def get_recipient_pk(self):
        return self.__payee_pk

    def get_transaction_hash(self):
        return self.__tx_hash

    def get_index(self):
        return self.__idx
