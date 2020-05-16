from typing import Dict

from util.message.advertise_self_message import AdvertiseSelfMessage
from util.message.ping_message import PingMessage
from util.peer_data import PeerData
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Model


def handle_broadcast_responses(self: 'Model', message, responses):
    handler = broadcast_handlers_binding[type(message)]
    handler(self, responses)


def new_peers_handler(self: 'Model', responses: Dict[str, PeerData]):
    for peer_data in responses.values():
        if peer_data is not None:
            self.active_peers.append(peer_data)


def ping_handler(self: 'Model', responses: Dict[str, PingMessage]):
    for ping in responses.values():
        if ping is not None:
            print(ping.msg)


broadcast_handlers_binding = {
    AdvertiseSelfMessage: new_peers_handler,
    PingMessage: ping_handler
}
