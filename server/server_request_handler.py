import threading
from queue import Queue

from server.event import Event


class ServerRequestHandler(threading.Thread):
    event: Event

    def __init__(self, request):
        threading.Thread.__init__(self)
        self.request = request

    def run(self):
        while True:
            print('[%s]: %s' % (self.request.client, self.request.message))
            self.request.response = input("You: ")
            with self.request.condition:
                self.request.condition.notify()
