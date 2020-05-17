import argparse
import pickle
import socket
import threading
from queue import Queue
from time import sleep
import requests
import yaml

import model
from client.broadcast_event import BroadcastEvent
from client.client_dispatcher import ClientDispatcher
from server.server_dispatcher import ServerDispatcher
from server.server_thread import ServerThread
from util.message.advertise_self_message import AdvertiseSelfMessage
from util.message.ping_message import PingMessage


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
    peers_address_database = get_peers_list()
    print(peers_address_database)

    model = model.Model(server_address())

    BUF_SIZE = 100
    server_queue = Queue(BUF_SIZE)
    server_thread = ServerThread(args.port, server_queue)
    server_dispatcher = ServerDispatcher(server_queue, model)

    server_thread.setDaemon(True)
    server_thread.start()
    server_dispatcher.setDaemon(True)
    server_dispatcher.start()

    broadcast_queue = Queue(BUF_SIZE)
    client_dispatcher = ClientDispatcher(broadcast_queue, model)
    client_dispatcher.setDaemon(True)
    client_dispatcher.start()

    advertise_event = BroadcastEvent(AdvertiseSelfMessage(model.peer_data), peers=peers_address_database)
    with advertise_event.condition:
        broadcast_queue.put(advertise_event)
        advertise_event.condition.wait()

    while True:
        msg = input("Enter message: ")
        if msg == '':
            continue
        advertise_event = BroadcastEvent(PingMessage(msg))
        with advertise_event.condition:
            broadcast_queue.put(advertise_event)
            advertise_event.condition.wait()

