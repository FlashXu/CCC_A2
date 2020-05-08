from redis import Redis, ConnectionPool
import json


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = Redis(**redis_kwargs)
        self.key = f'{namespace}:{name}'

    def __len__(self):
        return self.qsize()

    def __getitem__(self, i):
        return self.__db.lindex(self.key, i).decode()

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        if type(item) not in [int, float, str, bytes]:
            item = json.dumps(item)
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if isinstance(item, tuple):
            item = item[1]

        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)
