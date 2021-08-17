import random

from src._minion_helper import get_balance
from config import FRIENDS

def get_send_data(friends:dict):
    for friend in friends.items():
        friend: get_balance(friend[0])
    address = min(friends, key=friends.get)
    amount = random.randint(1, 3)
    name = FRIENDS[address]
    return address, amount, name
