from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from transaction.transaction import Transaction


class Client:

    def __init__(self):
        self.__secret_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1028,
            backend=default_backend()
        )
        self.public_key = self.__secret_key.public_key()
        self.__wallet = []

    # TODO: delete this method after integration
    def get_sk(self):
        return self.__secret_key

    # TODO: transaction generation mechanism
    def generate_tx(self, outputs):
        value = 0
        for pair in outputs:
            value += pair[1]
        total = 0
        inputs = []
        for ip in self.__wallet:
            total += ip.get_value()
            ip.sign(self.__secret_key)
            inputs.append(ip)
            if total >= value:
                break
        tx = Transaction(self.__secret_key, self.public_key, inputs, outputs, True)

    def maybe_store_output(self, block):
        for tx in block.transactions():
            for op in tx.get_outputs():
                if op.get_recipient_pk() == self.public_key:
                    self.__wallet.append(op)
