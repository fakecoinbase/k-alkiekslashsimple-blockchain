import hashlib
import datetime

from util.helpers import CHAIN_SIZE
from util import *
from transaction.transaction import Transaction
from chain.errors import InvalidTransactions
import util.helpers as helper


class Block:

    def __init__(self, height=-1, transactions=[], previous_hash="", timestamp=None, nonce=-1):
        """
       :param height: height # of block
       :type height: int
       :param transactions: list of transactions
       :type transactions: list of transaction objects
       :param previous_hash: previous block hash
       :type previous_hash: str
       :param timestamp: timestamp of block mined
       :type timestamp: int
       :param nonce: proof of work
       :type timestamp: int
       """
        self._height = height
        self._time_stamp = timestamp
        if timestamp is None:
            self._time_stamp = datetime.datetime.now()
        self._transactions = transactions
        self._previous_hash = previous_hash
        self._merkle_root = self._calculate_merkle_root()
        self._nonce = nonce
        self._block_size = CHAIN_SIZE
        self._block_hash = self._compute_hash()

    def _calculate_merkle_root(self):
        if len(self._transactions) < 1:
            raise InvalidTransactions(self._height, "Zero transactions in block. Coinbase transaction required")
        merkle_base = [helper.hash_transaction(t) for t in self.transactions]
        while len(merkle_base) > 1:
            temp_merkle_base = []
            for i in range(0, len(merkle_base), 2):
                if i == len(merkle_base) - 1:  # to hundle not power of two number of transactions
                    temp_merkle_base.append(
                        hashlib.sha256(merkle_base[i].encode('utf-8')).hexdigest()
                    )
                else:
                    temp_merkle_base.append(
                        hashlib.sha256(merkle_base[i].encode('utf-8') + merkle_base[i + 1].encode('utf-8')).hexdigest()
                    )
            merkle_base = temp_merkle_base
        return merkle_base[0]

    @property
    def block_size(self):
        return self._block_size

    @block_size.setter
    def block_size(self, bz):
        self._block_size = bz

    @property
    def block_height(self):
        return self._height

    @block_height.setter
    def block_height(self, bh):
        self._height = bh

    @property
    def block_hash(self):
        return self._block_hash

    @block_hash.setter
    def block_size(self, bh):
        self.self._block_hash = bh

    def _compute_hash(self):
        h = hashlib.sha256()
        h.update(
            str(self._nonce).encode('utf-8') +
            str(self.merkle_root).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self._time_stamp).encode('utf-8')
        )
        return h.hexdigest()

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

    @property
    def merkle_root(self):
        return self._merkle_root

    @merkle_root.setter
    def merkle_root(self, mr):
        self._merkle_root = mr

    def contains_transaction(self, transaction_id):
        for t in self.transactions:
            if helper.hash_transaction(t) == transaction_id:
                return True
        return False

    def hash_difficulty(self):
        difficulty = 0
        for c in self.block_hash:
            if c != '0':
                break
            difficulty += 1
        return difficulty

    def __str__(self):
        s = "Time stamp: " + str(self._time_stamp) + "\n"
        s = "Block Hash: " + str(self.block_hash()) + "\nBlockNo: " + str(self.block_height) + "\nBlock Data: \n"
        for tx in self.transactions:
            s += str(tx.to_dict()) + "\n"
        s += "Hashes: " + str(
            self.nonce) + "\n prevHash: " + self._previous_hash + "\n Merkle root: " + self.merkle_root \
             + "\n--------------"
        return s
