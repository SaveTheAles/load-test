import secrets
import base58
import pandas as pd
import requests
import random

from itertools import permutations
from config import CIDS_COUNT, LCD_API, MSGS
from cyberpy import privkey_to_address


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


def get_cross_link(privkey):
    address = privkey_to_address(privkey)
    block = int(requests.get(LCD_API + f'/blocks/latest').json()['block']['header']['height'])
    txs = requests.get(LCD_API + f'/txs?message.action=cyberlink&limit=10&tx.minheight={block - 100}').json()['txs']
    cleaned_txs = [tx for tx in txs if tx['logs'][0]['events'][1]['attributes'][0]['value'] != address]
    exctracted_cid = []
    for tx in cleaned_txs:
        exctracted_cid.extend(extract_cid(tx))
    exctracted_cid = list(set(exctracted_cid))
    perm = list(permutations(exctracted_cid, 2))
    random_choice = random.choices(perm, k=MSGS)
    return pd.DataFrame(random_choice, columns=['object_from', 'object_to'])


def extract_cid(tx):
    msgs = tx['tx']['value']['msg']
    objects = []
    for msg in msgs:
        links = msg['value']['links']
        for link in links:
            objects.append(link['from'])
            objects.append(link['to'])
    return list(set(objects))
