import threading
from queue import Queue

from request import Request


class ServerRequestHandler(threading.Thread):
    request: Request

    def __init__(self, request):
        threading.Thread.__init__(self)
        self.request = request

    def run(self):
        while True:
            print('[%s]: %s' % (self.request.client, self.request.message))
            self.request.response = input("You: ")
            with self.request.condition:
                self.request.condition.notify()
