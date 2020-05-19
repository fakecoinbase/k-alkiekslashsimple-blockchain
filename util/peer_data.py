from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class PeerData:
    def __init__(self, address, pk=None):
        self.address = address
        self.pk = pk

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def get_pk(self):
        if self.pk is None:
            return None
        return serialization.load_pem_public_key(self.pk, backend=default_backend())
