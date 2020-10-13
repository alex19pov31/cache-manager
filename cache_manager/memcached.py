import socket
from datetime import timedelta
from typing import Tuple, List, Union
import pickle
from cache_manager.base import CacheManager, BaseClient


class MemcachedClient(BaseClient):
    def set_data(self, key: str, data, expire: timedelta) -> bool:
        """Сохранение данных"""
        data_bytes: bytes = pickle.dumps(data)
        count_bytes: int = len(data_bytes)
        command: bytes = 'set {} 0 {} {}\r\n'.format(key, expire.seconds, count_bytes).encode('utf-8')
        command = b''.join([command, data_bytes, b'\r\n'])
        result_command: bytes = self._send_command(command)
        return result_command == b'STORED\r\n'

    def get_data(self, key: str):
        """Запрос данных по ключу"""
        command: bytes = 'get {}\r\n'.format(key).encode('utf-8')
        command_result: bytes = self._send_command(command)
        parts_result: List[bytes] = command_result.split(b'\r\n')
        if len(parts_result) < 3:
            return None

        data: bytes = parts_result[1]
        return pickle.loads(data)


class MemcachedCache(CacheManager):
    def __init__(self, addr: Union[Tuple[str, int], str]):
        self.client = MemcachedClient(addr)

    def _get_data(self, key: str):
        return self.client.get_data(key)

    def _save_data(self, data, key: str, ttl: timedelta):
        self.client.set_data(key, data, ttl)
