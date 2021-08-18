# load-test

## Usage

0. python3 and pip3 required

1. Install requirements

```bash
pip3 install -r requirements.txt
```

2. Fill the `config.py` file with the following credentials.

General info:

```python
LCD_API = '' # the LCD API endpoint without '/' in the end of string, on port 1317 by default
RPC_API = '' # the RPC API endpoint without '/' in the end of string, on port 26657 by default
HERO = '' # your hero moniker
MSGS = 25 # the amount of links in one transaction (max 25)
```

the bot character in percents:

```python
TYPE = {
    "cyberlinker": 90,
    "crosslinker": 5,
    "invalid_cyberlinker": 2,
    "sender": 3
}
```

make sure the sum of percents is 100.

the list of seed phrases of bots:

```python3
MINIONS = ['paste your seed phrase here',
           'paste your seed phrase here',
           'paste your seed phrase here',
           'paste your seed phrase here',
           'paste your seed phrase here',
           'paste your seed phrase here',
           'paste your seed phrase here',
           'paste your seed phrase here'
           ]
```

if you have less than 8 prepared addresses just remove the strings
leave bracket ']' in the end


3. Run:

```bash
python3 main.py
```

the output should be:

```
17/08/2021 15:55:52 Bot Bob made cyberlink, Sir! Result: 5787B68A462C2DCD0AACC136E21132B425BA65B358B73C97899A25189233CEA2
17/08/2021 15:55:52 Bot Alex made cyberlink, Sir! Result: 80CEDB879F728F1D01F3A6C398DC4BF8813C08B4283066B83AD582D825FAF7B0
17/08/2021 15:55:52 Bot Daniel made cyberlink, Sir! Result: BBFA72D409CF39E529C8DF129502B5CC065187D68079300C9520EEDB0CD069AB
17/08/2021 15:55:52 Bot Carl made crosslink, Sir! Result: DB56E910E485D26D7EA57F7DD6C08D61770F0E36CB63D4DCBAA3EB6A613CE152
```
