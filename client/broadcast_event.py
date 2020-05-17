from threading import Condition


class BroadcastEvent:
    condition: Condition

    def __init__(self, message, peers=None):
        self.condition = Condition()
        self.message = message
        self.peers = peers
        self.responses = {}

    def add_response(self, peer: str, response):
        self.responses[peer] = response
