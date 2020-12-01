import base58
import secrets
import pandas as pd
import requests

from config import *
from random import choice
from cyberpy import Transaction
from cyberpy import seed_to_privkey
from cyberpy import privkey_to_address

def get_sequence(address):
    request = requests.get(LCD_API+'/auth/accounts/{}'.format(address))
    return request.json()['result']['value']['sequence']

def get_number(address):
    request = requests.get(LCD_API+'/auth/accounts/{}'.format(address))
    return request.json()['result']['value']['account_number']

def generate_tx(seed):
    privkey = seed_to_privkey(seed, path="m/44'/118'/0'/0/0")
    address = privkey_to_address(privkey)
    account_num = get_number(address)
    sequence = get_sequence(address)
    return Transaction(
        privkey=privkey,
        account_num=account_num,
        sequence=sequence,
        fee=0,
        gas=200000,
        memo="",
        chain_id=CHAIN_ID,
        sync_mode="async",
    )

def get_random_hash():
    return secrets.token_hex(32)

def get_ipfs_hash(hash):
    if hash:
        hash_bytes = bytes.fromhex(hash)
        lenght = bytes([len(hash_bytes)])
        hash = b'\x12' + lenght + hash_bytes
        return base58.b58encode(hash).decode('utf-8')
    else:
        pass

def generate_cid_set():
    cids_count = LINK_SET
    cid_set = []
    for i in range(cids_count):
        cid_set.append(get_ipfs_hash(get_random_hash()))
    return cid_set

def generate_links_set():
    cid_set = generate_cid_set()
    object_from = []
    object_to = []
    for cid in cid_set:
        object_from.extend([cid] * (len(cid_set) - 1))
        object_to.extend([x for x in cid_set if x not in [cid]])
    return pd.DataFrame(list(zip(object_from, object_to)), columns=['object_from', 'object_to'])

def generate_txs(df):
    links = 0
    cids = []
    txs = []
    for account in ACCOUNTS:
        tx = generate_tx(account)
        cases = []
        for n in range(LINKS_IN_BLOCK):
            case_n = choice([i for i in range(0, df.shape[0] - 1) if i not in cases])
            cases.append(case_n)
            cids.append(df.loc[case_n]['object_from'])
            cids.append(df.loc[case_n]['object_to'])
            links +=1
            tx.add_cyberlink(cid_from = df.loc[case_n]['object_from'], cid_to = df.loc[case_n]['object_to'])
        pushable_tx = tx.get_pushable()
        txs.append(pushable_tx)
    return txs

def broadcast(txs):
    for tx in txs:
        res = requests.post(url=LCD_API + '/txs', data=tx)
        if res.status_code == 200:
            res = res.json()
            print(res)
        else:
            raise Exception("Broadcact failed to run by returning code of {}".format(res.status_code))