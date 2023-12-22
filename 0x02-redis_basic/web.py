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

cache = redis.Redis()


def access_count(method: Callable) -> Callable:
    """
    decorator for counting access frequency and caching it for 10s
    """
    @wraps(method)
    def wrapper(url):
        """decorator implementation"""
        # check if there is cached content and return it for slow connection
        content_key = "html:{}".format(url)
        counter_key = "count:{}".format(url)
        cache.incr(counter_key)

        data = cache.get(content_key)
        if data:
            return data.decode("utf-8")

        # cache is expired, fetch new content and cache it
        fresh_content = method(url)
        cache.set(content_key, fresh_content, ex=10)
        return fresh_content

    return wrapper


@access_count
def get_page(url: str) -> str:
    """
    tracks how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    results = get_page(url)
    print(results)
