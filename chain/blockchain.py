from chain.block import Block
from transaction.transaction import Transaction


class Blockchain():
    """
    Blockchain is a tree
    each node contain block
    depth
    """
    block_chain = []
    # TODO set configration for each block
    # MAX_SIZE = 0  # to be set
    # DIFFICULTY = 0

    # TODO don't forget to set height
    def __init__(self, block):
        self._block = block

    @property
    def block(self):
        return self._block

    def add_block(self, block):
        """
        Create a new Block in the Blockchain
        A block should have:
        * height
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block
        """
        if self._block.block_hash == block.previous_hash:
            new_chain = Blockchain(block)
            new_chain.block.block_height = self.block.block_height + 1
            self.block_chain.append(new_chain)

            return True
        for child in self.block_chain:
            if child.add_block(block):
                return True
        return False

    def get_block_of_transaction(self, tran_id):
        if self._block.contains_transaction(tran_id):
            return self
        curr = None
        for child in self.block_chain:
            curr = child.get_block_of_transaction(tran_id)
            if curr is not None:
                break
        return curr

    #longest tree path
    def get_head_of_chain(self):
        if not self.block_chain:
            return self
        maximum = 0
        curr = None
        for child in self.block_chain:
            d = child.depth()
            if d > maximum:
                maximum = d
                curr = child.get_head_of_chain()
        return curr

    def depth(self):
        if not self.block_chain:
            return 1
        maximum = 0
        for child in self.block_chain:
            d = child.depth()
            if d > maximum:
                maximum = d
        return maximum + 1

    def validate(self):
        pass