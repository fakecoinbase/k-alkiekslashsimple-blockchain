import random
from typing import List

from util.peer_data import PeerData


class Model:
    active_peers: List[PeerData]
    peer_data: PeerData

    def __init__(self, server_address):
        self.peer_data = PeerData(server_address, random.randint(1000000, 99999999))
        self.server_address = server_address
        self.active_peers = []

    from ._broadcast_handler import handle_broadcast_responses
    from ._server_handler import handle_server_message
