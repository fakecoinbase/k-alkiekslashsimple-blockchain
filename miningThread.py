import threading

from chain.block import Block


class MiningThread(threading.Thread):

    def __init__(self):
        super(MiningThread, self).__init__()
        self.__stop_event = threading.Event()
        self.__transactions = []
        self.__prev_hash = ""
        self.__diff = 0
        self.__block = None

    def set_data(self, transactions, prev_block_hash, difficulty):
        self.__transactions = transactions
        self.__prev_hash = prev_block_hash
        self.__diff = difficulty

    def get_block(self):
        return self.__block

    def stop(self):
        self.__stop_event.set()

    def stopped(self):
        return self.__stop_event.is_set()

    def run(self):
        pow_found = False
        nonce = 0
        block = None
        while not pow_found:
            if self.stopped():
                break
            block = Block(transactions=self.__transactions, previous_hash=self.__prev_hash, nonce=nonce)
            if block.hash_difficulty() == self.__diff:
                pow_found = True
            nonce += 1
        if pow_found:
            self.__block = block
