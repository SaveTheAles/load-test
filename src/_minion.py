import random

from cyberpy import seed_to_privkey
from src._minion_helper import *
from src._cyberlink import generate_links_set, get_double_link, get_cross_link
from src._send import get_send_data
from config import HERO, RPC_API, MSGS
from time import sleep


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

    def send(self):
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=send")
        send_data = get_send_data(self.friends)
        tx.add_transfer(recipient=send_data[0], amount=send_data[1], denom='mamper')
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.send, res)

    def cyberlink(self):
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=cyberlink")
        links_set = generate_links_set()
        links_set = links_set[:MSGS]
        for index, row in links_set.iterrows():
            tx.add_cyberlink(cid_from=row['object_from'], cid_to=row['object_to'])
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.cyberlink, res)

    def invalid_cyberlink(self):
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=invalid_cyberlink")
        link = get_double_link(self.account)
        tx.add_cyberlink(cid_from=link[0], cid_to=link[1])
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.invalid_cyberlink, res)

    def crosslink(self):
        tx = get_transaction(self.privkey, memo=f"load test, hero={HERO}, action=crosslink")
        links_set = get_cross_link(self.friends)
        for index, row in links_set.iterrows():
            tx.add_cyberlink(cid_from=row['object_from'], cid_to=row['object_to'])
        res = tx.broadcast(url=RPC_API)
        print_output(self.name, self.crosslink, res)

    # def delegate(self):
    #     tx = get_transaction(self.privkey)
    #     data = get_delegate_data()
    #     tx.add_delegation(validator=data[0], amount=data[1])
    #     res = tx.broadcast(url=LCD_API)
    #     print('----------------------------------------------------------------------')
    #     print('Soldier-bot {} made delegation to {} with {} euls, Sir!'.format(self.name, data[0], data[1]))
    #     print('Height:', res['height'])
    #     print('Hash:', res['txhash'])
    #
    # def redelegate(self):
    #     print('redelegating by', self.name)
    #
    # def undelegate(self):
    #     print('undelegating by', self.name)
    #
    # def withdraw(self):
    #     tx = get_transaction(self.privkey)
    #     validator = get_withdraw_validator(self.account)
    #     tx.add_withdraw(validator=validator)
    #     res = tx.broadcast(LCD_API=LCD_API)
    #     print('----------------------------------------------------------------------')
    #     print('Soldier-bot {} made withdraw, Sir!'.format(self.name))
    #     print('Height:', res['height'])
    #     print('Hash:', res['txhash'])

    def action(self):
        action = self._chose_action()
        if action == 'cyberlink':
            self.cyberlink()
        elif action == 'invalid_cyberlink':
            self.invalid_cyberlink()
        elif action == 'crosslink':
            self.crosslink()
        # elif action == 'delegate':
        #     self.delegate()
        # elif action == 'redelegate':
        #     self.redelegate()
        # elif action == 'undelegate':
        #     self.undelegate()
        # elif action == 'withdraw':
        #     self.withdraw()
        else:
            self.send()
        sleep(random.randint(5, 10))

    def _chose_action(self):
        case = random.randint(0, len(self.character) - 1)
        return self.character[case]
