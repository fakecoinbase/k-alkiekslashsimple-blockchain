import datetime
import collections
from typing import List

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from transaction.utxo import Utxo


class Transaction:
    __outputs: List[Utxo]

    def __init__(self, originator_pk, originator_sk, recipients, inputs, value, witnesses_included=True):
        """
        Constructor for the 'Transaction' class.
        :param originator_pk: public_key.
        :param originator_sk: secret_key.
        :param recipients: the recipient(s) public key.
        :param inputs: UTXO(s)
        :param value: value to be transferred.
        :param witnesses_included: flag.
        """
        self.__originator = originator_pk
        self.__sign_sk = originator_sk
        self.__recipients = recipients
        self.__inputs = inputs
        self.__timestamp = datetime.datetime.now()
        self.__witnesses_included = witnesses_included
        self.__value = value
        self.__signature = b''
        self.__generate_outputs()
        self.__witnesses = []
        if self.__witnesses_included:
            self.__set_witnesses()

    def to_dict(self):
        return collections.OrderedDict({
            'witnesses_included': self.__witnesses_included,
            'witnesses': self.__witnesses,
            'originator': self.__originator,
            'recipient': self.__recipients,
            'ip_counter': len(self.__inputs),
            'inputs': self.__inputs,
            'op_counter': len(self.__outputs),
            'outputs': self.__outputs,
            'time': self.__timestamp
        })

    def sign_transaction(self):
        # h = SHA256.new(str(self.to_dict()).encode('utf8'))
        # self.__signature = binascii.hexlify(self.__originator.signer.sign(h)).decode('ascii')
        self.__signature = self.__sign_sk.sign(
            data=str(self.to_dict()).encode('utf-8'),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hashes.SHA256()
        )

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
            outputs.append(Utxo(self, output_idx, transfer_val, rec))
            output_idx += 1
        if total_val - self.__value > 0:
            outputs.append(Utxo(self, output_idx, total_val - self.__value, self.__originator))
        self.__outputs = outputs

    # TODO: delete this method after integration
    def get_timestamp(self):
        return self.__timestamp

    # TODO: delete this method after integration
    def get_outputs(self):
        return self.__outputs

    def __set_witnesses(self):
        for ip in self.__inputs:
            self.__witnesses.append(ip.get_recipient_pk())

