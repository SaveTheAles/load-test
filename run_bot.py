import time
import random

from src._minion_helper import get_account_data


def run_bot(bot):
    while True:
        try:
            account_number, sequence = get_account_data(bot.account)
            for i in range(10):
                bot.action(account_number, sequence)
                sequence += 1
        except Exception as e:
            print(e)
            continue
        # time.sleep(random.randint(7, 10))
        time.sleep(6)

