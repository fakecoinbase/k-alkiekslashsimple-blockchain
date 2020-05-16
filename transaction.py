import binascii
import datetime
import collections
from typing import List

from Crypto.Hash import SHA

from utxo import Utxo


class Transaction:

    inputs: List[Utxo]

    def __init__(self, originator, recipients, inputs, value, witnesses_included=True):
        """
        Constructor for the 'Transaction' class.
        :param originator: client object.
        :param recipients: the recipient(s) public key.
        :param inputs: UTXO(s)
        :param value: value to be transferred.
        :param witnesses_included: flag.
        """
        self.originator = originator
        self.recipients = recipients
        self.inputs = inputs
        self.timestamp = datetime.datetime.now()
        self.witnesses_included = witnesses_included
        self.signature = None

    def to_dict(self):
        return collections.OrderedDict({
            'signature': self.signature,
            'witness_included': self.witnesses_included,
            'originator': self.originator.public_key,
            'recipient': self.recipients,
            'inputs': self.inputs,
            'time': self.timestamp
        })

    def sign_transaction(self):
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        self.signature = binascii.hexlify(self.originator.signer.sign(h)).decode('ascii')

    def get_signature(self):
        return self.signature

    def payee_pk(self):
        return self.recipient

    '''
        At the receiver side, verification can be done using the public part of the RSA key:
    
    >>> key = RSA.importKey(open('pubkey.der').read())
    >>> h = SHA.new(message)
    >>> verifier = PKCS1_v1_5.new(key)
    >>> if verifier.verify(h, signature):
    >>>    print "The signature is authentic."
    >>> else:
    >>>    print "The signature is not authentic."
    
    '''
