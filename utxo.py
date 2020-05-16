import transaction


class Utxo:

    def __init__(self, tx, op_index, value, pk):
        self.tx_signature = tx.get_signature()
        self.payee_pk = pk
        self.tx_hash = hash(tx)
        self.idx = op_index
        self.__value = value

    def get_value(self):
        return self.__value

    # TODO: verification