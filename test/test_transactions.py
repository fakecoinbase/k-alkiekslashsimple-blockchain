import unittest

from client import Client
from transaction import Transaction


class MyTestCase(unittest.TestCase):
    def test_client_creation(self):
        user = Client()
        self.assertIsInstance(user, Client)

    def test_transaction_creation(self):
        u1 = Client()
        u2 = Client()
        tx = Transaction(u1.public_key, u1.get_sk(), [u2.public_key], [], 5, False)
        self.assertIsInstance(tx, Transaction)

    def test_transaction_outputs(self):
        u1 = Client()
        u2 = Client()
        tx = Transaction(u1.public_key, u1.get_sk(), [u2.public_key], [], 5, False)
        outputs = tx.get_outputs()
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0].get_recipient_pk(), u2.public_key)

    def test_transaction_signing(self):
        u1 = Client()
        u2 = Client()
        tx = Transaction(u1.public_key, u1.get_sk(), [u2.public_key], [], 5, False)
        tx.sign_transaction()
        self.assertNotEqual(None, tx.get_signature())

    def test_transaction_dumping(self):
        u1 = Client()
        u2 = Client()
        tx = Transaction(u1.public_key, u1.get_sk(), [u2.public_key], [], 5, False)
        dictionary = tx.to_dict()
        self.assertEqual(dictionary['witness_included'], False)
        self.assertEqual(dictionary['originator'], u1.public_key)
        self.assertEqual(dictionary['recipient'], [u2.public_key])
        self.assertEqual(dictionary['ip_counter'], 0)
        self.assertEqual(dictionary['inputs'], [])
        self.assertEqual(dictionary['op_counter'], 1)
        self.assertEqual(dictionary['outputs'], tx.get_outputs())
        self.assertEqual(dictionary['time'], tx.get_timestamp())

    def test_transaction_verification(self):
        u1 = Client()
        u2 = Client()
        tx = Transaction(u1.public_key, u1.get_sk(), [u2.public_key], [], 5, False)
        tx.sign_transaction()
        u3 = Client()
        result = u3.validate_transaction(tx)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
