import threading
from queue import Queue


class ServerRequestDispatcher(threading.Thread):
    port: int
    queue: Queue

    def __init__(self, queue, server_address):
        threading.Thread.__init__(self)
        self.queue = queue
        self.server_address = server_address

    def run(self):
        while True:
            request = self.queue.get()
            with request.condition:
                # TODO: Invoke some handler for the request
                print('[%s]: %s' % (request.client, request.message))
                request.response = "echo back from %s: %s" % (self.server_address, request.message)
                request.condition.notify()
