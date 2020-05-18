import hashlib
import datetime


class Block:
    def __init__(self):
        self._time_stamp = datetime.datetime.now()
        self._transactions = []
        self._previous_hash = ""
        self._merkle_root = ""
        self._nonce = 0
        self._index = -1

    def __init__(self, previous_hash, merkle_root, timestamp=None, nonce=0, transactions=[]):
        self._time_stamp = timestamp
        if timestamp is None:
            self._time_stamp = datetime.datetime.now()
        self._transactions = transactions
        self._previous_hash = previous_hash
        self._merkle_root = merkle_root
        self._nonce = nonce
        self._index = -1

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def compute_hash(self):
        pass;

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, ts):
        self._time_stamp = ts

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, tr):
        self._transactions = tr

    @property
    def previous_hash(self):
        return self._previous_hash

    @previous_hash.setter
    def previous_hash(self, ph):
        self._previous_hash = ph

    @propertygit
    def merkle_root(self):
        return self._merkle_root

    @merkle_root.setter
    def merkle_root(self, mr):
        self._merkle_root = mr

    def __str__(self):
        s = "Time stamp: " + str(self._time_stamp) + "\n"
        s = "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self._index) + "\nBlock Data: \n"
        for tx in self.transactions:
            s += str(tx) + "\n"
        s += "Hashes: " + str(
            self.nonce) + "\n prevHash: " + self._previous_hash + "\n Merkle root: " + self.merkle_root + "\n-------------- "
        return s
