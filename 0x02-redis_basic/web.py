#!/usr/bin/env python3
"""
implement a get_page function (prototype: def get_page(url: str) -> str:).
The core of the function is to use the requests module to obtain the
HTML content of a particular URL and returns it.
"""
import requests
import redis
from functools import wraps
from typing import Callable


def access_count(method: Callable) -> Callable:
    """
    decorator for counting access frequency and caching it for 10s
    """
    @wraps(method)
    def wrapper(url):
        cache = redis.Redis()
        key = "count:{}".format(url)
        cache.incr(key)
        cache.expire(key, 10)
        return method(url)

    return wrapper


@access_count
def get_page(url: str) -> str:
    """
    tracks how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    response = requests.get(url)
    return response.text
