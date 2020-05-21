import random
import threading
from time import sleep
from typing import TYPE_CHECKING

from client.broadcast_event import BroadcastEvent
from transaction.transaction import Transaction
from util.helpers import P_DOUBLE_SPEND, CLIENT_SLEEP_TIME

if TYPE_CHECKING:
    from model import Model


class TransactionGenerator(threading.Thread):
    def __init__(self, model: 'Model'):
        super().__init__()
        self.model = model
        self.spent_inputs = []

    def run(self):
        while True:
            tx = self.generate_random_tx()
            if tx is not None:
                self.broadcast_transaction(tx)
            sleep(CLIENT_SLEEP_TIME)

    def broadcast_transaction(self, tx: Transaction):
        tx_event = BroadcastEvent(tx)
        # print(tx.get_peer_data().pk)
        self.model.broadcast_queue.put(tx_event)

    def generate_random_tx(self):
        if not self.model.get_wallet() or (random.random() < P_DOUBLE_SPEND and len(self.spent_inputs) > 0):
            input_utxo = random.choice(self.spent_inputs)
            print("============= Double spending an input! ============ ")
        else:
            input_utxo = self.model.get_random_input()
            self.model.get_wallet().remove(input_utxo)
            self.spent_inputs.append(input_utxo)

        value = input_utxo.get_value()

        n_outputs = 2
        pks = list(map(lambda x: x.pk, random.choices(self.model.peers_database, k=n_outputs)))
        output_values = [random.uniform(value * 0.49, value * 0.1) for _ in pks]
        change = value - sum(output_values)

        output_values.append(change)
        pks.append(self.model.peer_data.pk)
        outputs = list(zip(pks, output_values))

        return self.model.generate_tx(outputs, input_utxo)

