from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


class Client:

    def __init__(self):
        # # generate private/public key pair
        # key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)
        #
        # # get public key in OpenSSH format
        # public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        #
        # # get private key in PEM container format
        # pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
        #                         encryption_algorithm=serialization.NoEncryption())
        #
        # # decode to printable strings
        # private_key_str = pem.decode('utf-8')
        # public_key_str = public_key.decode('utf-8')
        self.__secret_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1028,
            backend=default_backend()
        )
        self.public_key = self.__secret_key.public_key()

        # self.signer = PKCS1_v1_5.new(self.__secret_key)

    # TODO: delete this method after integration
    def get_sk(self):
        return self.__secret_key

    def validate_transaction(self, tx):
        # Step #1:
        # make sure that the originator is the actual recipient of the input utxos
        signature = tx.get_signature()
        tx = tx.to_dict()
        public_key = tx['originator']
        for ip in tx['inputs']:
            if ip.get_recipient_pk() != public_key:
                print("Non matching recipient and originator.")
                return False
        # Step #2:
        # validate the signature of the originator
        # h = SHA256.new(str(tx).encode('utf8'))
        # verifier = PKCS1_v1_5.new(public_key)
        # if not verifier.verify(h, tx['signature']):
        #     return False
        # return True
        try:
            public_key.verify(
                signature=signature,
                data=str(tx).encode('utf-8'),
                padding=padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                algorithm=hashes.SHA256()
            )
        except InvalidSignature:
            print("Invalid Signature")
            return False
        return True
