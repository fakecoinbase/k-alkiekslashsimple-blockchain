import datetime
import collections

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from transaction.utxo import Utxo


class Transaction:

    def __init__(self, originator_pk, originator_sk, inputs, outputs, witnesses_included=True):
        """
        Constructor for the 'Transaction' class.
        :param originator_pk: public_key.
        :param originator_sk: secret_key.
        :param outputs: list of pairs(pk, value).
        :param inputs: UTXO(s)
        :param witnesses_included: flag.
        """
        self.__originator = originator_pk
        self.__sign_sk = originator_sk
        self.__inputs = inputs
        self.__timestamp = datetime.datetime.now()
        self.__witnesses_included = witnesses_included
        self.__witnesses = []
        if self.__witnesses_included:
            self.__set_witnesses()
        self.destinations = outputs
        self.__signature = b''
        self.__generate_outputs()

    def to_dict(self):
        return collections.OrderedDict({
            'originator': self.__originator,
            'witnesses_included': self.__witnesses_included,
            'witnesses': self.__witnesses,
            'ip_counter': len(self.__inputs),
            'inputs': self.__inputs,
            'op_counter': len(self.__outputs),
            'outputs': self.__outputs,
            'time': self.__timestamp
        })

    def sign_transaction(self):
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
        self.__outputs = []
        for pair in self.destinations:
            self.__outputs.append(Utxo(self, output_idx))
            output_idx += 1

    # TODO: delete this method after integration
    def get_timestamp(self):
        return self.__timestamp

    # TODO: delete this method after integration
    def get_outputs(self):
        return self.__outputs

    def __set_witnesses(self):
        for ip in self.__inputs:
            self.__witnesses.append(ip.get_transaction_hash())

