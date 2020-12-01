import time
from methods import generate_links_set, generate_txs, broadcast
from config import SLEEP_TIME

while True:
    start_time = time.time()
    txs = generate_txs(generate_links_set())
    broadcast(txs)
    end_time = time.time()
    time_taken = end_time - start_time
    print(" Time taken in seconds: {} s".format(time_taken))
    time.sleep(SLEEP_TIME)