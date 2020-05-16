import transaction


class Utxo:

    def __init__(self, tx, index, pk):
        """
        Constructor for the 'Utxo' class.
        :param tx: hash of the tx
        :param index:
        """
        self.tx = tx
        self.idx = index
        self.__value = 1

    def get_value(self):
        return self.__value

    # TODO: verification