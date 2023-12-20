#!/usr/bin/env python3
"""
This module defines a cache layer built on top of Redis for exploring redis
for basic operations and using it as a simple cache
"""
import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    decorator to count the number of times a function is called
    """
    @wraps(method)
    def wrapper(self: 'Cache', *args, **kwds):
        # get redis instance defined in Cache here
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """
    This is a cache implementation based on Redis
    """
    def __init__(self) -> None:
        """Initializes a redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores data in a Redis database using a random key and returns
        the key
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Union[Callable, None] = None) -> Any:
        """
        returns output in correct format
        """
        value = self._redis.get(key)
        if value is not None and fn is not None:
            decoded = fn(value)
            return decoded
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """convert byte stream to string"""
        return self.get(key, fn=lambda d: d.decode('utf8'))

    def get_int(self, key: str) -> Union[int, None]:
        """convert byte stream to int"""
        return self.get(key, fn=int)
