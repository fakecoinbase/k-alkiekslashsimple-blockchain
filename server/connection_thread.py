import pickle
import threading
from queue import Queue
from socket import socket

from server.event import Event


class ConnectionThread(threading.Thread):
    connection: socket
    queue: Queue

    def __init__(self, connection, client_address, queue):
        threading.Thread.__init__(self)
        self.connection = connection
        self.client_address = client_address
        self.queue = queue

    def run(self):
        try:
            print('connection from', self.client_address)
            # Receive message
            req = self.connection.recv(4096)
            request = pickle.loads(req)

            # Unpack and create event object
            event = Event(request, self.client_address)

            with event.condition:
                self.queue.put(event)
                event.condition.wait()

            # Receive the data in small chunks and retransmit it
            self.connection.sendall(pickle.dumps(event.response))

        finally:
            # Clean up the connection
            self.connection.close()
