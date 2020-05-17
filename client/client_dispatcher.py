import pickle
import socket
import threading
from queue import Queue

from model import Model
from util.helpers import recv_bytes, send_bytes


def broadcast(peers_addresses, message):
    responses = {}
    print('Broadcasting a', type(message).__name__)
    for peer_address in peers_addresses:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        ip, port = peer_address.split(':')
        try:
            sock.connect((ip, int(port)), )
            send_bytes(sock, pickle.dumps(message))
            reply = recv_bytes(sock)
            responses[peer_address] = pickle.loads(reply)
        except Exception as e:
            print('Could not send %s to %s' % (type(message).__name__, peer_address))
            responses[peer_address] = None
            print(e)
        finally:
            sock.close()
    return responses


class ClientDispatcher(threading.Thread):
    port: int
    queue: Queue

    def __init__(self, queue, model: Model):
        threading.Thread.__init__(self)
        self.model = model
        self.queue = queue

    def run(self):
        while True:
            event = self.queue.get()
            with event.condition:
                peers = event.peers or map(lambda p: p.address, self.model.active_peers)
                event.responses = broadcast(peers, event.message)
                self.model.handle_broadcast_responses(event.message, event.responses)
                event.condition.notify()
