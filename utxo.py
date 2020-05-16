import transaction


class Utxo:

    def __init__(self, txid):
        self.transaction_id = txid
