import random

from cyberpy import seed_to_privkey
from src._minion_helper import *
from src._cyberlink import generate_links_set, get_double_link, get_cross_link
from src._send import get_send_data
from config import HERO, RPC_API, CYBERLINKS_IN_TX


class Minion:
    def __init__(self,
                 seed: str,
                 character: list,
                 friends: dict,
                 name: str
                 ):
        self.seed = seed
        self.name = name
        self.privkey = seed_to_privkey(seed)
        self.account = privkey_to_address(self.privkey)
        self.character = character
        self.friends = friends
        self.balance = get_balance(self.account)

    def send(self, account_number, sequence):
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=send", account_number=account_number, sequence=sequence, gas=65_000)
        send_data = get_send_data(self.friends)
        tx.add_transfer(recipient=send_data[0], amount=send_data[1], denom='milliampere')
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.send, res)

    def cyberlink(self, account_number, sequence):
        gas = 80_000 + (CYBERLINKS_IN_TX * 22_000)
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=cyberlink", account_number=account_number, sequence=sequence, gas=int(gas))
        links_set = generate_links_set()
        links_set = list(links_set.itertuples(index=False, name=None))
        links_set = links_set[:CYBERLINKS_IN_TX]
        tx.add_chain_cyberlink(links_set)
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.cyberlink, res)

    def invalid_cyberlink(self, account_number, sequence):
        gas = 80_000
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=invalid_cyberlink", account_number=account_number, sequence=sequence, gas=int(gas))
        link = get_double_link(self.account)
        tx.add_cyberlink(cid_from=link[0], cid_to=link[1])
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.invalid_cyberlink, res)

    def crosslink(self, account_number, sequence):
        gas = 80_000 + (CYBERLINKS_IN_TX * 22_000)
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=crosslink", account_number=account_number, sequence=sequence, gas=int(gas))
        links_set = get_cross_link(self.privkey)
        links_set = list(links_set.itertuples(index=False, name=None))
        links_set = links_set[:CYBERLINKS_IN_TX]
        tx.add_chain_cyberlink(links_set)
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.crosslink, res)

    def action(self, account_number, sequence):
        action = self._chose_action()
        if action == 'cyberlink':
            self.cyberlink(account_number, sequence)
        elif action == 'invalid_cyberlink':
            self.invalid_cyberlink(account_number, sequence)
        elif action == 'crosslink':
            self.crosslink(account_number, sequence)
        else:
            self.send(account_number, sequence)

    def _chose_action(self):
        case = random.randint(0, len(self.character) - 1)
        return self.character[case]
