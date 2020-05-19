from typing import TYPE_CHECKING

from transaction.transaction import Transaction
from util.message import bft
from util.message.advertise_self_message import AdvertiseSelfMessage
from util.message.bft import PrePrepareMessage, PrepareMessage, CommitMessage
from util.message.ping_message import PingMessage
from util.message.success_response import SuccessResponse

if TYPE_CHECKING:
    from model import Model


class ServerHandler:
    def __init__(self, model: 'Model'):
        self.model = model

    @property
    def server_handlers_binding(self):
        return {
            AdvertiseSelfMessage: self.new_peer_handler,
            PingMessage: self.ping_handler,
            bft.PrePrepareMessage: self.bft_pre_prepare_handler,
            bft.PrepareMessage: self.bft_prepare_handler,
            bft.CommitMessage: self.bft_commit_handler,
            Transaction: self.transaction_handler
        }

    def handle(self, message):
        handler = self.server_handlers_binding[type(message)]
        response = handler(message)
        return response

    def new_peer_handler(self, message: AdvertiseSelfMessage):
        self.model.active_peers.append(message.peer_data)
        print(self.model.active_peers)
        return self.model.peer_data

    def ping_handler(self, message: PingMessage):
        print(message.msg)
        return PingMessage('received by: ' + self.model.peer_data.address)

    def bft_pre_prepare_handler(self, message: PrePrepareMessage):
        self.model.bft_context.pre_prepare(message)
        return SuccessResponse()

    def bft_prepare_handler(self, message: PrepareMessage):
        self.model.bft_context.prepare(message)
        return SuccessResponse()

    def bft_commit_handler(self, message: CommitMessage):
        self.model.bft_context.commit(message)
        return SuccessResponse()

    def transaction_handler(self, message: Transaction):
        print(message)
        if self.model.mode == 'miner':
            print(message.to_dict())
            self.model.add_transaction(message)
        return SuccessResponse()

