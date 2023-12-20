#!usr/bin/env python3
"""
This module defines a cache layer built on top of Redis for exploring redis
for basic operations and using it as a simple cache
"""
import redis
from typing import Union
import uuid


class Cache:
    """
    This is a cache implementation based on Redis
    """
    _redis: redis.Redis

    def __init__(self) -> None:
        """Initializes a redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        stores data in a Redis database using a random key and returns
        the key
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
