import argparse
from time import sleep
import grpc
import blockchain_pb2_grpc
from blockchain_pb2 import PingMsg
from server_thread import ServerThread


def parse_args():
    parser = argparse.ArgumentParser(description='Simple blockchain client-server')
    parser.add_argument('mode', type=str, choices=['miner', 'client'], default='miner',
                        help='mode for the client-server to operate in')
    parser.add_argument('-p', '--port', dest='port', default=9980, help='port number for the server')
    parser.add_argument('-pc', '--peer-configs', dest='peers path', default='./peer-configs',
                        help='peer configurations file')
    parser.add_argument('-c', '--consensus', dest='algorithm', type=str, choices=['pow', 'bft'], default='pow',
                        help='consensus algorithm to use')
    parser.add_argument('-t', '--transactions', dest='transactions path', default=None,
                        help='path to transactions file to be used. If not provided, random transactions will be '
                             'generated')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    self_address = '197.135.207.32:' + str(args.port)

    peers = ['197.135.207.32:9980', '197.135.207.32:9981', '197.135.207.32:9982', '197.135.207.32:9983']

    peers.remove(self_address)
    server_thread = ServerThread(args.port)
    server_thread.start()

    channels = [grpc.insecure_channel(peer) for peer in peers]
    stubs = [blockchain_pb2_grpc.BlockchainServiceStub(channel) for channel in channels]

    while True:
        for stub, peer in zip(stubs, peers):
            ping_msg = PingMsg(msg="hello")
            print('pinging', peer, ' :', ping_msg.msg)
            try:
                reply = stub.Ping(ping_msg)
                print('reply:', reply.msg)
            except grpc._channel._InactiveRpcError:
                print(peer, 'not online')
        sleep(5)
