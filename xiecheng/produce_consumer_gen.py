import threading


class ThreadSafeGenerator:
    def __init__(self, gen):
        self.gen = gen
        self.lock = threading.Lock()

    def __iter__(self):
        return self.next()

    def next(self):
        with self.lock:
            return self.gen.next()

    def send(self, inform):
        with self.lock:
            return self.gen.send(inform)


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        for i in range(1000):
            a = i+1
        print('Consumer consuming...', n)
        r = '200 OK'


def producer(con):
    con.send(None)
    n = 0
    while True:
        n += 1
        print("Producing .....", n)
        r = con.send({'abc': 1, 'bcd':2})
        print("Consumer return ...", r)


if __name__ == '__main__':
    """ if the generator has concurrent access issue, add lock"""
    c = ThreadSafeGenerator(consumer())
    # c = consumer()
    producer(c)
