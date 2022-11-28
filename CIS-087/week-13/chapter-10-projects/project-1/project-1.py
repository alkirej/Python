"""
File: producerconsumer2.py
Producer-consumer demo with synchronization.
Producer and consumer both access shared data a given number
of times. They sleep a random interval before each access.
The data must be produced before it is consumed, and be produced
and consumed just once.
The condition and Boolean flag on the shared data guarantee that
the producer and consumer access the data in the correct order.
"""

import time, random
from threading import Thread, currentThread, Condition

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class SharedCell(object):
    """Shared data that sequences writing before reading."""

    def __init__(self):
        """Can produce but not consume at startup."""
        self.data = -1
        self.writeable = True
        self.ok_to_write = Condition()
        self.readable = False
        self.done_reading = Condition()

    def setData(self, data):
        """Second caller must wait until someone has
        consumed the data before resetting it."""
        thread_name = currentThread().getName()
        self.ok_to_write.acquire()
        while not self.writeable:
            self.ok_to_write.wait()
        while len(self.done_reading._waiters)>0:
            time.sleep(1)
        print("\n%s setting data to %d" % (thread_name, data))
        self.data = data
        self.writeable = False
        self.readable = True

        self.ok_to_write.notify()
        self.ok_to_write.release()

    def getData(self, thread_count):
        """Caller must wait until someone has produced
        the data before accessing it."""
        thread_name = currentThread().getName()
        self.ok_to_write.acquire()
        while self.writeable:
            self.ok_to_write.wait()
        self.ok_to_write.notify()
        self.ok_to_write.release()

        self.done_reading.acquire()
        if len(self.done_reading._waiters) >= thread_count-1:
            self.readable = False
            self.done_reading.notify_all()
            self.writeable = True

            # Notify writer it is ok to proceed.
            self.ok_to_write.acquire()
            self.ok_to_write.notify()
            self.ok_to_write.release()

        while self.readable:
            self.done_reading.wait()

        self.done_reading.release()
        return self.data

class Producer(Thread):
    """A producer of data in a shared cell."""

    def __init__(self, cell, accessCount):
        Thread.__init__(self, name = "Producer")
        self.accessCount = accessCount
        self.cell = cell

    def run(self):
        """Resets the data in the cell and goes to sleep,
        the given number of times."""
        print("%s starting up" % self.getName())
        for count in range(self.accessCount):
            self.cell.setData(count + 1)
            time.sleep(1)
        print("%s is done producing\n" % self.getName())

class Consumer(Thread):
    """A consumer of data in a shared cell."""

    def __init__(self, cell, thread_num, accessCount, thread_count):
        Thread.__init__(self, name = "Consumer #%d" % thread_num )
        self.accessCount = accessCount
        self.cell = cell
        self.thread_count = thread_count

    def run(self):
        """Accesses the data in the cell and goes to sleep,
        the given number of times."""
        print("%s starting up\n" % self.getName())
        for count in range(self.accessCount):
            value = self.cell.getData(self.thread_count)
            print("  %s consumed %d" % (self.getName(),value))
        print("%s is done consuming\n" % self.getName())

def main():
    accessCount = int(input("Enter the number of accesses: "))
    thread_count = int(input("Enter the number of consumers: "))
    cell = SharedCell()
    print("Starting Producer")
    p = Producer(cell, accessCount)
    p.start()
    print("Starting Consumers")
    for n in range(thread_count):
        c = Consumer(cell, n+1, accessCount, thread_count)
        c.start()

if __name__ == "__main__":
    main()
