import grpc

import blockchain_pb2_grpc
from blockchain_pb2 import PongMsg, PingMsg


# noinspection PyMethodMayBeStatic
class BlockchainServicer(blockchain_pb2_grpc.BlockchainServiceServicer):

    def Ping(self, request: PingMsg, context:grpc.ServicerContext):
        print(context.peer(), 'pinged', request.msg)
        pong = PongMsg(msg=request.msg + ' pong')
        return pong
