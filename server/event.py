from threading import Condition


class Event:
    condition: Condition

    def __init__(self, message, client=None):
        self.condition = Condition()
        self.message = message
        self.client = client
        self.response = None

    def set_response(self, response):
        self.response = response
