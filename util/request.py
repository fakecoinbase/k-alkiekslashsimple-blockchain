from threading import Condition


class Request:
    condition: Condition

    def __init__(self, condition, message, client=None):
        self.condition = condition
        self.message = message
        self.client = client
        self.response = None

    def set_response(self, response_msg):
        self.response = response_msg
