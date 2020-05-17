from block import Block
class Blockchain():

    def __init__(self, size):
        self.MAX_SIZE = size   # instance variable unique to each instance
        self.chain = ""

    def create_block(self):
        """
        Create a new Block in the Blockchain
        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        return new Block()
    def add_and_validate_block(self):
        pass
    def validate(self):
        pass