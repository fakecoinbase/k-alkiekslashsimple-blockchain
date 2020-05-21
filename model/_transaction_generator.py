import random
import threading
from time import sleep
from typing import TYPE_CHECKING

from client.broadcast_event import BroadcastEvent
from transaction.transaction import Transaction

if TYPE_CHECKING:
    from model import Model


class TransactionGenerator(threading.Thread):
    def __init__(self, model: 'Model'):
        super().__init__()
        self.model = model

    def run(self):
        while True:
            tx = self.generate_random_tx()
            self.broadcast_transaction(tx)
            sleep(2)

    def broadcast_transaction(self, tx: Transaction):
        tx_event = BroadcastEvent(tx)
        # print(tx.get_peer_data().pk)
        self.model.broadcast_queue.put(tx_event)

    def generate_random_tx(self):
        input_utxo = self.model.get_random_input()
        # self.model.get_wallet().remove(input_utxo)
        value = input_utxo.get_value()

        n_outputs = 2
        pks = list(map(lambda x: x.pk, random.choices(self.model.peers_database, k=n_outputs)))
        output_values = [random.uniform(value * 0.05, value * 0.1) for _ in pks]
        change = value - sum(output_values)

        output_values.append(change)
        pks.append(self.model.peer_data.pk)
        outputs = list(zip(pks, output_values))

        return self.model.generate_tx(outputs, input_utxo)

