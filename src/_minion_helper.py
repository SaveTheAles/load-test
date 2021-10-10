import requests


from datetime import datetime
from config import LCD_API, CHAIN_ID, SYNC_MODE
from cyberpy import Transaction, privkey_to_address


def get_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def get_account_data(address: str, url: str = LCD_API, print_message: bool = False):
    _res = requests.get(f'{url}/cosmos/auth/v1beta1/accounts/{address}')
    try:
        _account_number = int(_res.json()['account']['account_number'])
        _sequence = int(_res.json()['account']['sequence'])
    except KeyError:
        _account_number = int(_res.json()['account']['base_vesting_account']['base_account']['account_number'])
        _sequence = int(_res.json()['account']['base_vesting_account']['base_account']['sequence'])
    if print_message:
        print(f'address: {address}\naccount number: {_account_number}\nsequence: {_sequence}')
    return _account_number, _sequence


def get_validators(address):
    res = requests.get(LCD_API + '/staking/delegators/' + address + '/delegations').json()['result']
    validators = {}
    for validator in res:
        temp = {
            validator['validator_address']: int(validator['balance']['amount'])
        }
        validators.update(temp)
    return validators


def get_balance(address):
    balances = requests.get(LCD_API + '/cosmos/bank/v1beta1/balances/' + address).json()['balances']
    amper = list(filter(lambda denom: denom['denom'] == 'milliampere', balances))[0]
    return int(amper['amount'])


def get_transaction(privkey, memo, gas=80_000, fee=0, account_number=False, sequence=False):
    if not account_number or not sequence:
        _account_number, _sequence = get_account_data(privkey_to_address(privkey))
        return Transaction(
            privkey=privkey,
            account_num=_account_number,
            sequence=_sequence,
            fee=fee,
            gas=gas,
            memo=memo,
            chain_id=CHAIN_ID,
            sync_mode=SYNC_MODE,
        )
    else:
        _account_number, _sequence = account_number, sequence
        return Transaction(
            privkey=privkey,
            account_num=_account_number,
            sequence=_sequence,
            fee=0,
            gas=gas,
            memo=memo,
            chain_id=CHAIN_ID,
            sync_mode=SYNC_MODE,
        )


def print_output(name, function, res):
    if res["result"]["code"] == 0:
        print(get_time(), f'Bot {name} made {function.__name__}, Sir! Result: {res["result"]["hash"]}')
    else:
        print(get_time(), f'Bot {name} ERROR with {function.__name__}, Sir! Result: code={res["result"]["code"]}, codespace: {res["result"]["codespace"]}, log: {res["result"]["log"]}')