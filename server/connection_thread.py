import pickle
import threading
from queue import Queue
from socket import socket

from server.event import Event
from util.helpers import recv_bytes, send_bytes


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
            req = recv_bytes(self.connection)
            request = pickle.loads(req)

            # Unpack and create event object
            event = Event(request, self.client_address)

            with event.condition:
                self.queue.put(event)
                event.condition.wait()

            # Receive the data in small chunks and retransmit it
            send_bytes(self.connection, pickle.dumps(event.response))
        finally:
            # Clean up the connection
            self.connection.close()
