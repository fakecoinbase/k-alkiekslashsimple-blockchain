import transaction
import Crypto.Random as CRand
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Client:

    def __init__(self):
        random = CRand.new().read
        self.__secret_key = RSA.generate(1024, random)
        self.public_key = self.__secret_key.publickey()
        self.signer = PKCS1_v1_5.new(self.__secret_key)


utxo = []
u1 = Client()
u2 = Client()
initial_tx = transaction(u2, u1.public_key, utxo, )
tx = transaction(u1, u2.public_key, transaction(u1, u2))