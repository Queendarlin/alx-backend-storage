#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """Caches the output of fetched data and tracks request counts.
    """

    @wraps(method)
    def invoker(url) -> str:
        """The wrapper function for caching the output and tracking the count.
        """
        # Increment the count of URL accesses
        count_key = f'count:{url}'
        result_key = f'result:{url}'
        redis_store.incr(count_key)

        # Check if the result is already cached
        result = redis_store.get(result_key)
        if result:
            return result.decode('utf-8')

        # If not cached, fetch the result and
        # cache it with an expiration time of 10 seconds
        result = method(url)
        redis_store.setex(result_key, 10, result)
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    return requests.get(url).text


# Testing the get_page function
if __name__ == "__main__":
    test_url = "http://google.com"

    # First call, should fetch and cache
    print("First call:", get_page(test_url))

    # Second call within 10 seconds, should return cached result
    print("Second call:", get_page(test_url))

    # Display the count of accesses
    count = redis_store.get(f"count:{test_url}").decode('utf-8')
    print(f"Access count for {test_url}: {count}")

    # Wait for 11 seconds to ensure the cache expires
    import time

    time.sleep(11)

    # Third call after cache expiration, should fetch and cache again
    print("Third call after cache expiration:", get_page(test_url))

    # Display the count of accesses again
    count = redis_store.get(f"count:{test_url}").decode('utf-8')
    print(f"Access count for {test_url}: {count}")
