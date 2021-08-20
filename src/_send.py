import random

from src._minion_helper import get_balance
from config import FRIENDS

def get_send_data(friends:dict):
    res = []
    for friend in friends.items():
        res.append((friend[0], int(get_balance(friend[0]))))
    address = min(res, key=lambda x: x[1])[0]
    amount = random.randint(1, 3)
    name = FRIENDS[address]
    return address, amount, name
