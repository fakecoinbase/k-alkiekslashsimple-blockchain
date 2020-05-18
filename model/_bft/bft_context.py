from typing import List, TYPE_CHECKING

from model._bft.bft_state import IdleState, BFTState
from util.message.bft import PrePrepareMessage, PrepareMessage, CommitMessage

if TYPE_CHECKING:
    from model import Model


class BFTContext:
    state: BFTState
    pre_prepare_message: PrePrepareMessage
    prepare_messages: List[PrepareMessage]
    commit_messages: List[CommitMessage]

    def __init__(self, peers: list, model, leader=False):
        self.reset()
        self.peers = peers
        self.model = model
        self.leader = leader

    # noinspection PyTypeChecker
    def reset(self):
        self.state = IdleState(self)
        self.pre_prepare_message = None
        self.prepare_messages = []
        self.commit_messages = []

    def pre_prepare(self, message):
        self.state.pre_prepare(message)

    def prepare(self, message):
        self.state.prepare(message)

    def commit(self, message):
        return self.state.commit(message)

    def transition_to(self, state_class: BFTState.__class__):
        self.state = state_class(self)

    @property
    def tolerated_faults(self):
        return (len(self.peers) - 1) / 3
