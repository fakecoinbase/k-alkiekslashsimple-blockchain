import Crypto.Random as CRand
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


def validate_transaction(tx):
    # Step #1:
    # make sure that the originator is the actual recipient of the input utxos
    tx = tx.to_dict
    public_key = tx['originator']
    for ip in tx['inputs']:
        if ip.get_recipient_pk() != public_key:
            return False
    # Step #2:
    # validate that the signature of the originator
    h = SHA256.new(str(tx).encode('utf8'))
    verifier = PKCS1_v1_5.new(public_key)
    if not verifier.verify(h, tx['signature']):
        return False
    return True


class Client:

    def __init__(self):
        random = CRand.new().read
        self.__secret_key = RSA.generate(1024, random)
        self.public_key = self.__secret_key.publickey()
        self.signer = PKCS1_v1_5.new(self.__secret_key)
