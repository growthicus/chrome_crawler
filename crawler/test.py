from queue import Queue
import threading
import time


class main:
    def __init__(self):
        self.q = Queue()

    def start(self):
        self.q.put(1)
        while True:
            c = self.q.get()
            w = worker(q=self.q)
            w.start()
            print(c)


class worker(threading.Thread):
    def __init__(self, q: Queue):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        time.sleep(3)
        for i in range(1, 5):
            self.q.put(1)


m = main()
m.start()
