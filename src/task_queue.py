
class TaskQueue:
    """ Queue for set task parameters"""

    def __init__(self, capacity):
        self.front = self.size = 0
        self.rear = capacity - 1
        self.Q = [None] * capacity
        self.capacity = capacity

    def is_full(self):
        return self.size == self.capacity

    def is_empty(self):
        return self.size == 0

    def enqueue(self, item):
        if self.is_full():
            print("Full")
            return
        self.rear = (self.rear + 1) % (self.capacity)
        self.Q[self.rear] = item
        self.size = self.size + 1
        print("% s enqueued to queue" % str(item))

    def dequeue(self):
        if self.is_empty():
            print("Empty")
            return

        item = self.Q[self.front]
        print("% s dequeued from queue" % str(item))
        self.front = (self.front + 1) % (self.capacity)
        self.size = self.size - 1
        return item

    def que_front(self):
        if self.is_empty():
            print("Queue is empty")

        print("Front item is", self.Q[self.front])
        return self.Q[self.front]

    def que_rear(self):
        if self.is_empty():
            print("Queue is empty")
        print("Rear item is", self.Q[self.rear])
        return self.Q[self.rear]
