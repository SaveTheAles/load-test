from src._minion import Minion
from config import MINIONS, FRIENDS, CHARACTER
from cyberpy import seed_to_privkey, privkey_to_address
from multiprocessing import Process
from run_bot import run_bot

def main():
    minions = []
    procs = []

    for seed in MINIONS:
        name = FRIENDS[privkey_to_address(seed_to_privkey(seed))]
        friends = {k: FRIENDS[k] for k in FRIENDS.keys() - {privkey_to_address(seed_to_privkey(seed))}}
        minion = Minion(seed=seed, character=CHARACTER, friends=friends, name=name)
        minions.append(minion)

    for minion in minions:
        proc = Process(target=run_bot, args=(minion,))
        procs.append(proc)
    try:
        for proc in procs:
            proc.start()

        for proc in procs:
            proc.join()

    except KeyboardInterrupt:
        for proc in procs:
            proc.terminate()

if __name__ == '__main__':
    main()