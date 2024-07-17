#!/usr/bin/env python3
"""Redis module"""
import redis
import requests
from typing import Callable
from functools import wraps

# Initialize the Redis connection
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count how many times a URL was accessed.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs) -> str:
        # Increment the access count
        redis_client.incr(f"count:{url}")
        # Call the original method
        return method(url, *args, **kwargs)
    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of the function with an expiration time.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str, *args, **kwargs) -> str:
            # Check if the URL content is already cached
            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            # If not cached, call the original method to get the result
            result = method(url, *args, **kwargs)
            # Cache the result with an expiration time
            redis_client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator


@count_requests
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL and return it.
    """
    response = requests.get(url)
    return response.text
