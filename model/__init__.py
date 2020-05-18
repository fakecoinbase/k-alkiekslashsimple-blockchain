import random
from typing import List

from model._broadcast_handler import BroadcastHandler
from model._server_handler import ServerHandler
from util.peer_data import PeerData


class Model:
    active_peers: List[PeerData]
    peer_data: PeerData

    def __init__(self, server_address):
        self.peer_data = PeerData(server_address, random.randint(1000000, 99999999))
        self.server_address = server_address
        self.active_peers = []
        self.server_handler = ServerHandler(self)
        self.broadcast_handler = BroadcastHandler(self)

    def handle_broadcast_responses(self, message, responses):
        return self.broadcast_handler.handle(message, responses)

    def handle_server_message(self, message):
        return self.server_handler.handle(message)


