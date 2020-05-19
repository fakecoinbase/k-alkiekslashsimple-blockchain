from typing import Dict, TYPE_CHECKING

from model._bft.bft_state import PrePreparedState
from transaction.transaction import Transaction
from util.message import bft
from util.message.advertise_self_message import AdvertiseSelfMessage
from util.message.ping_message import PingMessage
from util.message.success_response import SuccessResponse
from util.peer_data import PeerData

if TYPE_CHECKING:
    from model import Model


class BroadcastHandler:
    def __init__(self, model: 'Model'):
        self.model = model

    @property
    def broadcast_handlers_binding(self):
        return {
            AdvertiseSelfMessage: self.new_peers_handler,
            PingMessage: self.ping_handler,
            bft.PrePrepareMessage: self.bft_pre_prepare_handler,
            bft.PrepareMessage: self.bft_prepare_handler,
            bft.CommitMessage: self.bft_commit_handler,
            Transaction: self.new_transaction_handler
        }

    def handle(self, message, responses):
        handler = self.broadcast_handlers_binding[type(message)]
        handler(responses)

    def new_peers_handler(self, responses: Dict[str, PeerData]):
        for peer_data in responses.values():
            if peer_data is not None:
                self.model.active_peers.append(peer_data)

    def ping_handler(self, responses: Dict[str, PingMessage]):
        for ping in responses.values():
            if ping is not None:
                print(ping.msg)

    def bft_pre_prepare_handler(self, responses: Dict[str, SuccessResponse]):
        pass
        # success_count = len(list(filter(lambda x: x is not None, responses.values())))
        # if success_count >= len(self.model.active_peers)/3:

    def bft_prepare_handler(self, responses: Dict[str, SuccessResponse]):
        pass

    def bft_commit_handler(self, responses: Dict[str, SuccessResponse]):
        pass

    def new_transaction_handler(self, responses: Dict[str, SuccessResponse]):
        print("transaction responses:", responses)
