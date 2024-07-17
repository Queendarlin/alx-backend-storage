#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count.
        """
        key = method.__qualname__

        # Increment the count
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class to interact with Redis"""

    def __init__(self):
        """Initialize the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) ->\
            Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis using the key and convert it
        using fn if provided.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis using the key.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis using the key.
        """
        return self.get(key, lambda d: int(d))
