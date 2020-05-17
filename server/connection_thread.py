import threading
from queue import Queue
from socket import socket

from util.request import Request


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
            msg = self.connection.recv(4096)

            # Unpack and create request object
            condition = threading.Condition()
            request = Request(condition, msg.decode(), self.client_address)

            with condition:
                self.queue.put(request)
                condition.wait()

            # Receive the data in small chunks and retransmit it
            self.connection.sendall(request.response.encode())

        finally:
            # Clean up the connection
            self.connection.close()
