import time
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread

import grpc
import blockchain_pb2_grpc
from blockchain_servicer import BlockchainServicer
from blockchain_pb2 import PongMsg, PingMsg


class ServerThread(Thread):

    def __init__(self, port, max_workers=10):
        super().__init__()
        self.server = grpc.server(ThreadPoolExecutor(max_workers=max_workers))
        blockchain_pb2_grpc.add_BlockchainServiceServicer_to_server(BlockchainServicer(), self.server)
        self.server.add_insecure_port('localhost:' + str(port))

    def run(self):
        self.server.start()
        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.server.stop(0)
        # finally:
        #     raise KeyboardInterrupt
