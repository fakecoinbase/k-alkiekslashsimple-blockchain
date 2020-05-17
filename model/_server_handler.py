from util.message.advertise_self_message import AdvertiseSelfMessage

from typing import TYPE_CHECKING

from util.message.ping_message import PingMessage

if TYPE_CHECKING:
    from model import Model


def handle_server_message(self: 'Model', message):
    handler = server_handlers_binding[type(message)]
    response = handler(self, message)
    return response


def new_peer_handler(self: 'Model', message: AdvertiseSelfMessage):
    self.active_peers.append(message.peer_data)
    return self.peer_data


def ping_handler(self: 'Model', message: PingMessage):
    print(message.msg)
    return PingMessage('received by: ' + self.server_address)


server_handlers_binding = {
    AdvertiseSelfMessage: new_peer_handler,
    PingMessage: ping_handler
}
