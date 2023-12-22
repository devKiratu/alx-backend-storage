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
    func_name = method.__qualname__
    @wraps(method)
    def wrapper(self: 'Cache', *args, **kwds):
        # get redis instance defined in Cache here
        self._redis.incr(func_name)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs and outputs for a
    particular function
    """
    @wraps(method)
    def wrapper(self: 'Cache', *args, **kwds):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        # store inputs
        self._redis.rpush(input_key, str(args))

        # store output
        output = method(self, *args, *kwds)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    displays the history of calls of a particular function fn.
    """
    cache = redis.Redis()
    fn_name = fn.__qualname__
    inputs = cache.lrange("{}:inputs".format(fn_name), 0, -1)
    outputs = cache.lrange("{}:outputs".format(fn_name), 0, -1)

    print("{} was called {} times".format(fn_name, len(list(inputs))))
    for i, j in list(zip(inputs, outputs)):
        try:
            input = i.decode('utf8')
            output = j.decode('utf8')
            print("{}(*{}) -> {}".format(fn_name, input, output))
        except Exception:
            print("{}(*{}) -> {}".format(fn_name, "", ""))


class Cache:
    """
    This is a cache implementation based on Redis
    """
    def __init__(self) -> None:
        """Initializes a redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
