import threading
import socket
from queue import Queue

from server.connection_thread import ConnectionThread


class ServerThread(threading.Thread):
    port: int
    queue: Queue

    def __init__(self, port, queue):
        threading.Thread.__init__(self)
        self.port = port
        self.queue = queue

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', self.port)
        print('starting up on %s port %s' % server_address)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while True:
            connection, client_address = sock.accept()
            ConnectionThread(connection, client_address, self.queue).start()
