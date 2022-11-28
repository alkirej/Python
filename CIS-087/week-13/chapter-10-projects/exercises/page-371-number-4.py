"""
File: sharedcell.py
Resource for shared data synchonization for the readers and writers
problem. Guarantees that a writer finishes writing before readers can
read and other writers can write. Also supports concurrent reading.
"""

from threading import Condition

class PCCell(object):
    """Synchronizes readers and writers around shared data,
    to support thread-safe reading and writing."""

    def __init__(self, data):
        """Sets up the conditions and count of active readers."""
        self.data = data
        self.producing = False
        self.consuming = False
        self.ot_to_consume = Condition()
        self.ok_to_produce = Condition()

    def begin_consumption(self):
        """Waits until a writer is not writing or the writers
        condition queue is empty. Then increments the reader
        count and notifies the next waiting reader."""
        self.ok_to_consume.acquire()
        self.ok_to_produce.acquire()
        while self.producing or len(self.ok_to_produce._waiters) > 0:
            self.ok_consume.wait()
        self.consuming = True
        self.ok_to_consume.notify()

    def end_consumption(self):
        """Notifies a waiting writer if there are
        no active readers."""
        self.consuming = False
        self.ok_to_produce.notify()
        self.ok_to_produce.release()
        self.ok_to_consume.release()

    def begin_produce(self):
        """Can write only when someone else is not
        writing and there are no readers are ready."""
        self.ok_to_produce.acquire()
        self.ok_to_consume.acquire()
        while self.producing or self.consuming:
            self.okToWrite.wait()
        self.producing = True

    def endWrite(self):
        """Notify the next waiting writer if the readers
        condition queue is empty. Otherwise, notify the
        next waiting reader."""
        self.producing = False
        if len(self.ok_to_consume._waiters) > 0:
            self.ok_to_consume.notify()
        else:
            self.ok_to_produce.notify()
        self.ok_to_consume.release()
        self.ok_to_produce.release()

    def consume(self, readerFunction):
        """Observe the data in the shared cell."""
        self.beginRead()
        # Enter reader's critical section
        result = readerFunction(self.data)
        # Exit reader's critical section
        self.endRead()
        return result

    def produce(self, writerFunction):
        """Modify the data in the shared cell."""
        self.beginWrite()
        # Enter writer's critical section
        result = writerFunction(self.data)
        # Exit writer's critical section
        self.endWrite()
        return result
