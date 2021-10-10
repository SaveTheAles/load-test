from cyberpy import seed_to_privkey, privkey_to_address

LCD_API = 'http://lcd_api' 
RPC_API = 'http://rpc_api'
HERO = 'your hero name'
CYBERLINKS_IN_TX = 1
TXS_IN_BLOCK = 5

CHAIN_ID = 'bostrom-testnet-4'
SYNC_MODE = 'broadcast_tx_sync'

TYPE = {
    "cyberlinker": 2,
    "crosslinker": 1,
    "invalid_cyberlinker": 2,
    "sender": 97
}

# MAX 8
MINIONS = ['bot1 seed phrase here',
           'bot2 seed phrase here',
           'bot3 seed phrase here',
           'bot4 seed phrase here',
           'bot5 seed phrase here',
           'bot6 seed phrase here',
           'bot7 seed phrase here',
           'bot8 seed phrase here'
           ]


# ----------------------------------------------------------
# ------------------ DO NOT TOUCH SECTION ------------------
# ----------------------------------------------------------

CIDS_COUNT = 15
NAMES = ['Alex', 'Bob', 'Carl', 'Daniel', 'Egor', 'Francis', 'Gerald', 'Harry', 'Igor', 'Jackob']
FRIENDS = {privkey_to_address(seed_to_privkey(minion)): name for minion, name in zip(MINIONS, NAMES)}
CHARACTER = ['cyberlink'] * (TYPE['cyberlinker'] * 100) + \
            ['crosslink'] * (TYPE['crosslinker'] * 100) + \
            ['invalid_cyberlink'] * (TYPE['invalid_cyberlinker'] * 100) + \
            ['send'] * (TYPE['sender'] * 100)
            # ['delegate'] * (TYPE['delegator'] * 100) + \
            # ['undelegate'] * (TYPE['undelegator'] * 100) + \
            # ['redelegate'] * (TYPE['redelegator'] * 100) + \
            # ['withdraw'] * (TYPE['withdrawer'] * 100)


if CYBERLINKS_IN_TX > 200:
    CYBERLINKS_IN_TX = 200
