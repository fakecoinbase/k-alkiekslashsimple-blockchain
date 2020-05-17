from typing import Dict

from util.message.advertise_self_message import AdvertiseSelfMessage
from util.message.ping_message import PingMessage
from util.peer_data import PeerData


class BroadcastHandler:
    def __init__(self, model):
        self.model = model

    @property
    def broadcast_handlers_binding(self):
        return {
            AdvertiseSelfMessage: self.new_peers_handler,
            PingMessage: self.ping_handler
        }

    def handle(self, message, responses):
        handler = self.broadcast_handlers_binding[type(message)]
        handler(responses)

    def new_peers_handler(self, responses: Dict[str, PeerData]):
        for peer_data in responses.values():
            if peer_data is not None:
                self.model.active_peers.append(peer_data)

    def ping_handler(self, responses: Dict[str, PingMessage]):
        for ping in responses.values():
            if ping is not None:
                print(ping.msg)
