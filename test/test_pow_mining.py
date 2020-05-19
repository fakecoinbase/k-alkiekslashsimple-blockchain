import unittest

from miner import Miner


class MyTestCase(unittest.TestCase):
    def test_miner_creation(self):
        miner_node = Miner()
        self.assertIsInstance(miner_node, Miner)

if __name__ == '__main__':
    unittest.main()
