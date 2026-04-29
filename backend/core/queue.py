# This could handle internal memory queues or interface with Redis directly if needed.
# Since we are using Celery, this might be a wrapper or used for specific internal batching.

class TaskQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, task):
        self.queue.append(task)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0
