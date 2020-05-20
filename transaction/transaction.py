import datetime
import collections
from transaction.utxo import Utxo


class Transaction:

    def __init__(self, outputs, peer_data=None, inputs=None, witnesses_included=False, timestamp=None):
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
        if timestamp is None:
            self.__timestamp = datetime.datetime.now()
        else:
            self.__timestamp = timestamp
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
            'inputs': list(map(lambda x: x.to_dict(), self.__inputs)),
            'op_counter': len(self.__outputs),
            'outputs': list(map(lambda x: x.to_dict(), self.__outputs)),
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

    def get_inputs(self):
        return self.__inputs

    def __set_witnesses(self):
        for ip in self.__inputs:
            self.__witnesses.append(ip.get_signature())

    def get_peer_data(self):
        return self.__peer_data

    def __eq__(self, other):
        return self.__signature == other.__signature
