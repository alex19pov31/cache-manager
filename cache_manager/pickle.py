import os
import pickle
from datetime import timedelta, datetime
from .base import CacheManager


class PickleCache(CacheManager):

    def _get_data(self, key: str):
        data = None
        file_path: str = os.path.join(self.storage_path, f'{key}.pickle')
        if not os.path.isfile(file_path):
            return None

        with open(file_path, 'rb') as f:
            cached_data: dict = pickle.load(f)
            time_exp = cached_data.get('time_exp', None)
            if not time_exp or time_exp <= datetime.now():
                return None

            data = cached_data.get('data', None)

        return data

    def _save_data(self, data, key: str, ttl: timedelta):
        cached_data: dict = {
            'data': data,
            'key': key,
            'time_exp': datetime.now() + ttl
        }

        file_path: str = os.path.join(self.storage_path, f'{key}.pickle')
        dir_name: str = os.path.dirname(file_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(cached_data, f)