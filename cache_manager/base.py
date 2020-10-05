import hashlib
import pickle
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Callable


class CacheManager(ABC):
    def __init__(self, storage_path: str = '.cache'):
        self.storage_path: str = storage_path

    def __call__(self, ttl: timedelta, key: str = None):
        def __(func: Callable):
            async def wrapper(*args, **kwargs):
                cache_key: str = key or hashlib.md5(pickle.dumps({
                    'args': args,
                    'kwargs': kwargs,
                    'func_name': func.__name__
                })).hexdigest()

                cached_data = self._get_data(cache_key)
                if cached_data is not None:
                    return cached_data

                data = await func(*args, **kwargs)
                self._save_data(data, cache_key, ttl)
                return data
            return wrapper
        return __

    @abstractmethod
    def _get_data(self, key: str):
        pass

    @abstractmethod
    def _save_data(self, data, key: str, ttl: timedelta):
        pass
