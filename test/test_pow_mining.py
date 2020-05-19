import unittest

from miner import Miner
from node import Client


class MyTestCase(unittest.TestCase):
    def test_miner_creation(self):
        miner_node = Miner()
        self.assertIsInstance(miner_node, Miner)

    def test_client_genesis_block(self):
        user_node = Client()
        self.assertEqual(user_node.wallet_size(), 1)

    def test_mining_one_block_one_miner(self):
        # block chain size is set to 5
        miner_node = Miner()
        user_node1 = Client()
        user_node2 = Client()
        user_node3 = Client()
        tx1 = user_node1.generate_tx([(user_node2.public_key, 5)],
                                     user_node1.get_random_input().get_transaction_hash(), 1)
        miner_node.add_transaction(tx1)
        tx2 = user_node1.generate_tx([(user_node3.public_key, 5)],
                                     user_node1.get_random_input().get_transaction_hash(), 1)
        miner_node.add_transaction(tx2)
        tx3 = user_node2.generate_tx([(user_node3.public_key, 5)],
                                     user_node2.get_random_input().get_transaction_hash(), 1)
        miner_node.add_transaction(tx3)
        tx4 = user_node2.generate_tx([(user_node1.public_key, 5)],
                                     user_node2.get_random_input().get_transaction_hash(), 1)
        miner_node.add_transaction(tx4)
        tx5 = user_node3.generate_tx([(user_node1.public_key, 5)],
                                     user_node3.get_random_input().get_transaction_hash(), 1)
        miner_node.add_transaction(tx5)
        self.assertTrue(miner_node.is_mining())

    def test_double_spending(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
