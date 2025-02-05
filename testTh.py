import threading
import time


EVENT = threading.Event()

def test():
    while not EVENT.is_set():
        time.sleep(2)
        print('hehe')


threading.Thread(target=test).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    EVENT.set()
    print('stop')
