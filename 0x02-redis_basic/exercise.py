#!/usr/bin/env python3
"""Module for redis caching"""

import redis
import uuid
from typing import Callable, Optional, Union


class Cache:
    """
    Cache class to interact with Redis for storing and retrieving data,
    counting method calls, and maintaining a history of inputs and outputs.
    """

    def __init__(self):
        """
        Initialize the Cache instance with a Redis connection.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the key and
        optionally apply a conversion function (fn) to the retrieved data.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Convenience method to retrieve a string value from Redis.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Convenience method to retrieve an integer value from Redis.
        """
        return self.get(key, fn=int)


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called
    using Redis INCR command.
    """
    count_key = f"{method.__qualname__}:calls"

    def wrapper(self, *args, **kwargs):
        self._redis.incr(count_key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a method
    using Redis lists.
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    def wrapper(self, *args, **kwargs):
        # Store inputs as a string in Redis list
        self._redis.rpush(inputs_key, str(args))
        # Execute the original method to get the output
        output = method(self, *args, **kwargs)
        # Store output as a string in Redis list
        self._redis.rpush(outputs_key, str(output))
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Function to display the history of calls of a particular function.
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode('utf-8')}) ->\
{out.decode('utf-8')}")


# Decorate Cache.store with count_calls decorator and call_history decorator
Cache.store = count_calls(call_history(Cache.store))
