
class TaskQueue:
    """ Queue for set task parameters for O(1) time complexity and O(n) space complexity"""

    def __init__(self, capacity):
        self.front = self.size = 0
        self.rear = capacity - 1
        self.Q = [None] * capacity
        self.capacity = capacity

    def is_full(self):
        """
        Returns True if queue is full, false otherwise
        """
        return self.size == self.capacity

    def is_empty(self):
        """
        Returns True if queue is empty, false otherwise
        """
        return self.size == 0

    def enqueue(self, item):
        """
        Adds task to the queue
        returns True if task is enqueued, false otherwise
        """
        if self.is_full():
            return False

        self.rear = (self.rear + 1) % self.capacity
        self.Q[self.rear] = item
        self.size = self.size + 1
        return True

    def dequeue(self):
        """
        Removes task from start of queue
        Returns None if queue is empty
        """
        if self.is_empty():
            return None

        item = self.Q[self.front]
        print("% s dequeued from queue" % str(item))
        self.front = (self.front + 1) % (self.capacity)
        self.size = self.size - 1
        return item

    def que_front(self):
        """
        Returns value at front of queue
        """
        if self.is_empty():
            return None

        return self.Q[self.front]

    def que_rear(self):
        """
        Returns value at back of queue
        """
        if self.is_empty():
            return None

        return self.Q[self.rear]
