class PeerData:
    def __init__(self, address, pk):
        self.address = address
        self.pk = pk

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()
