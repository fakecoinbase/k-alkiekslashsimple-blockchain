import argparse
import socket
import threading
from queue import Queue
from time import sleep
import requests
import yaml

from server.ServerRequestDispatcher import ServerRequestDispatcher
from server.server_thread import ServerThread


def parse_args():
    parser = argparse.ArgumentParser(description='Simple blockchain client-server')
    parser.add_argument('mode', type=str, choices=['miner', 'client'], default='miner',
                        help='mode for the client-serverssd to operate in')
    parser.add_argument('-p', '--port', dest='port', type=int, default=9980, help='port number for the server')
    parser.add_argument('-pl', '--peers-list', dest='peers_path', default='./peers.yaml',
                        help='peers list yaml file')
    parser.add_argument('-c', '--consensus', dest='algorithm', type=str, choices=['pow', 'bft'], default='pow',
                        help='consensus algorithm to use')
    parser.add_argument('-t', '--transactions', dest='transactions path', default=None,
                        help='path to transactions file to be used. If not provided, random transactions will be '
                             'generated')
    return parser.parse_args()


def get_peers_list():
    peer_dicts = []
    with open(args.peers_path, 'r') as file:
        peers_yaml = yaml.load(file, Loader=yaml.FullLoader)
        peer_dicts = peers_yaml['peers']

    peers_list = []
    for peer_dict in peer_dicts:
        ip, start_port, count = peer_dict['ip'], peer_dict['start_port'], peer_dict['count']
        peers_list.extend(['%s:%d' % (ip, port) for port in range(start_port, start_port + count)])

    peers_list.remove(server_address())
    return peers_list


def server_address():
    self_ip = requests.get('https://api.ipify.org').text
    # self_ip = 'localhost'
    print(self_ip)
    return self_ip + ':' + str(args.port)


if __name__ == '__main__':
    args = parse_args()
    peers = get_peers_list()
    print(peers)
    server_cond = threading.Condition()

    BUF_SIZE = 100
    server_queue = Queue(BUF_SIZE)
    ServerThread(args.port, server_queue).start()
    server_dispatcher = ServerRequestDispatcher(server_queue, server_address())
    server_dispatcher.start()

    i = 0
    while True:
        for peer in peers:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            ip, port = peer.split(':')
            try:
                sock.connect((ip, int(port)), )
                msg = 'ping' + str(i)
                i += 1
                sock.sendall(msg.encode())
                print('sending "%s" to %s' % (msg, peer))
                reply = sock.recv(4096)
                print("reply:", reply.decode())
            except Exception:
                print('cannot connect to', peer)
            finally:
                sock.close()
        sleep(2)
