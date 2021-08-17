import time

def run_bot(bot):
    while True:
        bot.action()
        time.sleep(7)

