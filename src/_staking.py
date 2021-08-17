import requests
import random

from config import LCD_API
from src._minion_helper import get_validators

def get_withdraw_validator(address):
    res = requests.get(LCD_API + '/distribution/delegators/{}/rewards'.format(address)).json()
    rewards = res['result']['rewards']
    result = {}
    for reward in rewards:
        if reward['reward']:
            temp = {reward['validator_address']: int(float(reward['reward'][0]['amount']))}
        else:
            temp = {reward['validator_address']: 0}
        result.update(temp)
    return max(result, key=result.get)

def get_delegate_data():
    res = requests.get(LCD_API+'/staking/validators').json()
    active_validators = res['result']
    operator_addresses = {active_validator['operator_address']: active_validator['tokens'] for active_validator in active_validators}
    validator = min(operator_addresses, key=operator_addresses.get)
    amount = random.randint(10, 100)
    return validator, amount

def get_redelegate_data(address):
    current_validators = list(get_validators(address))
    res = requests.get(LCD_API+'/staking/validators').json()['result']
    all_active_validators = [x['operator_address'] for x in res]
    possible_validators = [current_validators not in all_active_validators]



def get_unbond_data(address):
    pass

