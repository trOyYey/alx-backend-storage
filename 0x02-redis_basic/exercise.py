#!/usr/bin/env python3
"""
basic redis tasks
"""
from typing import Union, Optional, Callable, Any
import redis
import uuid
from functools import wraps


def replay(method: Callable) -> None:
    """
    display the history of calls of a particular function.

    Parameters:
        method: The function to display the history of.
    """
    name = method.__qualname__
    client = redis.Redis()
    inputs = client.lrange(f"{name}:inputs", 0, -1)
    outputs = client.lrange(f"{name}:outputs", 0, -1)
    print(f'{name} was called {len(inputs)} times:')
    for input, output in zip(inputs, outputs):
        print(f"{name}(*{input.decode('utf-8'}) -> {output.decode('utf-8')}")

def count_calls(method: Callable) -> Callable:
    """
    decorator that takes a single method Callable argument
    and returns a Callable.

    Parameters:
        fn: The function to be called.

    Returns:
        The decorated function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Increments the number of times the decorated function is called.

        Parameters:
            self: The instance of the Cache class.
            *args: The arguments to be passed to the decorated function.
            **kwargs: The keyword arguments to be passed to the decorated

        Returns:
            The return value of the decorated function.
        """
        if isinstance(self, Cache) and isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Returns the history of calls to the decorated function.

    Parameters:
        method: The function to be called.

    Returns:
        The decorated function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Returns the history of calls to the decorated function.

        Parameters:
            self: The instance of the Cache class.
            *args: The arguments to be passed to the decorated function.
            **kwargs: The keyword arguments to be passed to the decorated

        Returns:
            The return value of the decorated function.
        """
        input = "{}:inputs".format(method.__qualname__)
        output = "{}:outputs".format(method.__qualname__)
        return_value = method(self, *args, **kwargs)

        if isinstance(self, Cache) and isinstance(self._redis, redis.Redis):
            self._redis.rpush(input, str(args))
            self._redis.rpush(output, return_value)
        return return_value
    return wrapper


class Cache:
    """
    Cache class.

    This class is a wrapper around the Redis cache database.
    It provides a simple interface to store and retrieve data
    from the cache.
    """

    def __init__(self) -> None:
        """
        Initializes the cache class by creating a new Redis connection
        and removing any data in the db.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Saves the data in to the Redis db and returns
        the key to the value.

        Parameters:
            data: The data stored in the cache.

        Returns:
            The key to the data stored in the cache.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        method that take a key string argument and an
        optional Callable argument named fn.

        Parameters:
            key: The key linked with the stored data.
            fn: A function that convert the data back to the desired format.

        Returns:
            The stored data linked with the key in the desired format
        """
        data: bytes = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
         automatically parametrize Cache.get with the correct
         conversion function

        Parameters:
            key: key linked with the stored data.

        Returns:
            data stored converted into str.
        """
        value = self.get(key)
        if value is None:
            return None
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
         automatically parametrize Cache.get with the correct
         conversion function

        Parameters:
            key: The key linked with the stored data.

        Returns:
            data stored as int.
        """
        value = self.get(key)
        if value is None:
            return None
        return int(value)
