from util.message.advertise_self_message import AdvertiseSelfMessage
from util.message.ping_message import PingMessage


class ServerHandler:
    def __init__(self, model):
        self.model = model

    @property
    def server_handlers_binding(self):
        return {
            AdvertiseSelfMessage: self.new_peer_handler,
            PingMessage: self.ping_handler
        }

    def handle(self, message):
        handler = self.server_handlers_binding[type(message)]
        response = handler(message)
        return response

    def new_peer_handler(self, message: AdvertiseSelfMessage):
        self.model.active_peers.append(message.peer_data)
        print(self.model.active_peers)
        return self.model.peer_data

    def ping_handler(self, message: PingMessage):
        print(message.msg)
        return PingMessage('received by: ' + self.model.server_address)
