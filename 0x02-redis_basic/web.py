#!/usr/bin/env python3
"""
implement a get_page function (prototype: def get_page(url: str) -> str:).
The core of the function is to use the requests module to obtain the
HTML content of a particular URL and returns it.
"""
import requests
import redis


def get_page(url: str) -> str:
    """
    tracks how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    cache = redis.Redis()
    content_key = "html:{}".format(url)
    counter_key = "count:{}".format(url)
    # increment url counter
    cache.incr(counter_key)

    # check if there is cached content and return it for slow connection
    data = cache.get(content_key)
    if data:
        return data.decode("utf-8")

    # cache is expired, fetch new content and cache it
    response = requests.get(url)
    fresh_content = response.text
    cache.set(content_key, fresh_content, ex=10)
    return fresh_content
