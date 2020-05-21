import threading
from queue import Queue


class ServerDispatcher(threading.Thread):
    port: int
    queue: Queue

    def __init__(self, queue, model):
        threading.Thread.__init__(self)
        self.queue = queue
        self.model = model

    def run(self):
        while True:
            event = self.queue.get()
            with event.condition:
                print('Received ', type(event.message).__name__)
                message = event.message
                response = self.model.handle_server_message(message)
                event.response = response
                event.condition.notify()
