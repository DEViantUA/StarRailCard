# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import cachetools

class Cache:
    _cache = None

    @classmethod
    def get_cache(cls, maxsize: int = 100, ttl: int = 60) -> cachetools.TTLCache:
        """
        Returns the cache instance, creating it if necessary.

        Args:
            maxsize (int, optional): Maximum number of items the cache can hold. Defaults to 100.
            ttl (int, optional): Time-to-live for cached items in seconds. Defaults to 60.

        Returns:
            cachetools.TTLCache: The cache instance.
        """
        if cls._cache is None:
            cls._cache = cachetools.TTLCache(maxsize=maxsize, ttl=ttl)
        return cls._cache

    @classmethod
    def clear_cache(cls):
        """
        Clears the cache.
        """
        if cls._cache is not None:
            cls._cache.clear()
            cls._cache = None

    @classmethod
    def setting(cls, maxsize: int = 100, ttl: int = 60) -> cachetools.TTLCache:
        """
        Setting the cache.
        """
        cls._cache = cachetools.TTLCache(maxsize=maxsize, ttl=ttl)
    
    @classmethod
    def get(cls, key):
        """
        Retrieves a value from the cache by key.

        Args:
            key: The key of the value to retrieve.

        Returns:
            Any: The value associated with the key, or None if the key is not found in the cache.
        """
        if cls._cache is not None:
            return cls._cache.get(key)

    @classmethod
    def set(cls, key, value):
        """
        Sets a value in the cache with the specified key.

        Args:
            key: The key to set.
            value: The value to associate with the key.
        """
        if cls._cache is not None:
            cls._cache[key] = value

    @classmethod
    def delete(cls, key):
        """
        Deletes a value from the cache by key.

        Args:
            key: The key of the value to delete.
        """
        if cls._cache is not None and key in cls._cache:
            del cls._cache[key]

    @classmethod
    def contains(cls, key):
        """
        Checks if the cache contains a value with the specified key.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key is found in the cache, otherwise False.
        """
        if cls._cache is not None:
            return key in cls._cache
        return False
