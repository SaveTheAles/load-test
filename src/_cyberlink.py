import secrets
import base58
import pandas as pd
import requests
import random

from config import CIDS_COUNT, LCD_API


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
    cids_count = CIDS_COUNT
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


def get_double_link(address):
    res = requests.get(LCD_API + f'/txs?message.action=cyberlink&cybermeta.subject={address}&limit=1').json()
    tx = res['txs'][0]
    link = tx['tx']['value']['msg'][0]['value']['links'][0]
    return link['from'], link['to']


def get_cross_link(friends: dict):
    friend = random.choice(list(friends))
    res = requests.get(LCD_API + f'/txs?message.action=cyberlink&cybermeta.subject={friend}&limit=1').json()
    random_link = random.randint(1, int(res['total_count']))
    cross_tx = requests.get(LCD_API + f'/txs?message.action=cyberlink&cybermeta.subject={friend}&page={random_link}&limit=1').json()
    tx = cross_tx['txs'][0]
    object_from = [x['value']['links'][0]['from'] for x in tx['tx']['value']['msg']]
    object_to = [x['value']['links'][0]['to'] for x in tx['tx']['value']['msg']]
    return pd.DataFrame(list(zip(object_from, object_to)), columns=['object_from', 'object_to'])