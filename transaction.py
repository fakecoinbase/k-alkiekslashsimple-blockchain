import binascii
import datetime
import collections
from Crypto.Hash import SHA256

from utxo import Utxo


class Transaction:

    def __init__(self, originator, recipients, inputs, value, witnesses_included=True):
        """
        Constructor for the 'Transaction' class.
        :param originator: client object.
        :param recipients: the recipient(s) public key.
        :param inputs: UTXO(s)
        :param value: value to be transferred.
        :param witnesses_included: flag.
        """
        self.__originator = originator
        self.__recipients = recipients
        self.__inputs = inputs
        self.__timestamp = datetime.datetime.now()
        self.__witnesses_included = witnesses_included
        self.__value = value
        self.__signature = None
        self.__generate_outputs()

    def to_dict(self):
        return collections.OrderedDict({
            'signature': self.__signature,
            'witness_included': self.__witnesses_included,
            'originator': self.__originator.public_key,
            'recipient': self.__recipients,
            'ip_counter': len(self.__inputs),
            'inputs': self.__inputs,
            'op_counter': len(self.__outputs),
            'outputs': self.__outputs,
            'time': self.__timestamp
        })

        #       At the receiver side, verification can be done using the public part of the RSA key:
        #
        #   >>> key = RSA.importKey(open('pubkey.der').read())
        #   >>> h = SHA.new(message)
        #   >>> verifier = PKCS1_v1_5.new(key)
        #   >>> if verifier.verify(h, signature):
        #   >>>    print "The signature is authentic."
        #   >>> else:
        #   >>>    print "The signature is not authentic."

    def sign_transaction(self, pk=None):
        # assert (pk, self.__originator.public_key)
        h = SHA256.new(str(self.to_dict()).encode('utf8'))
        self.__signature = binascii.hexlify(self.__originator.signer.sign(h)).decode('ascii')

    def get_signature(self):
        return self.__signature

    def __generate_outputs(self):
        output_idx = 1
        total_val = 0
        outputs = []
        for unspent_tx in self.__inputs:
            total_val += unspent_tx.get_value()
        transfer_val = self.__value / len(self.__recipients)
        for rec in self.__recipients:
            outputs.append(Utxo(self, output_idx, transfer_val, rec.public_key))
            output_idx += 1
        outputs.append(Utxo(self, output_idx, total_val - self.__value, self.__originator.public_key))
        self.__outputs = outputs

    # TODO: transaction verification
    # TODO: signature verification


