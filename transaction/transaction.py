import datetime
import collections
from transaction.utxo import Utxo


class Transaction:

    def __init__(self, outputs, peer_data=None, inputs=None, witnesses_included=False):
        """
        Constructor for the 'Transaction' class.
        :param originator_pk: public_key.
        :param outputs: list of pairs(pk, value).
        :param inputs: UTXO(s)
        :param witnesses_included: flag.
        """
        if inputs is None:
            inputs = []
        self.__peer_data = peer_data
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
            'witnesses_included': self.__witnesses_included,
            'witnesses': self.__witnesses,
            'ip_counter': len(self.__inputs),
            'inputs': self.__inputs,
            'op_counter': len(self.__outputs),
            'outputs': self.__outputs,
            'time': self.__timestamp
        })

    def sign_transaction(self, signature):
        self.__signature = signature

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

    def get_outputs(self):
        return self.__outputs

    def __set_witnesses(self):
        for ip in self.__inputs:
            self.__witnesses.append(ip.get_signature())

    def get_peer_data(self):
        return self.__peer_data
