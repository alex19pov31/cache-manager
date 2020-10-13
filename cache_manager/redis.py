import pickle
from datetime import timedelta
from typing import Tuple, List, Union
from cache_manager.base import BaseClient, CacheManager


class RedisClient(BaseClient):
    def __init__(self, addr: Union[Tuple[str, int], str], timeout: int = 1, password: str = None):
        self.password = password
        super().__init__(addr, timeout)

    def __auth(self) -> bool:
        if not self.password:
            return False

        command: bytes = self.__prepare_command([
            b'AUTH',
            self.password.encode('utf-8')
        ])
        result_command: bytes = self._send_command(command, False)
        return result_command == b'+OK\r\n'

    def _connect(self):
        super(RedisClient, self)._connect()
        self.__auth()

    def set_data(self, key: str, data, expire: timedelta) -> bool:
        """Сохранение данных"""
        data_bytes: bytes = pickle.dumps(data)
        command: bytes = self.__prepare_command([
            b'SET',
            key.encode('utf-8'),
            data_bytes,
            b'EX',
            str(expire.seconds).encode('utf-8')
        ])
        result_command: bytes = self._send_command(command)
        return result_command == b'+OK\r\n'

    def get_data(self, key: str):
        """Запрос данных по ключу"""
        command: bytes = self.__prepare_command([
            b'GET',
            key.encode('utf-8')
        ])

        command_result: bytes = self._send_command(command)
        parts_result: List[bytes] = command_result.split(b'\r\n')
        if len(parts_result) < 3:
            return None

        data: bytes = parts_result[1]
        return pickle.loads(data)

    def __prepare_command(self, parts_command: List[bytes]) -> bytes:
        new_parts_command: List[bytes] = [f'*{len(parts_command)}'.encode('utf-8')]
        for part in parts_command:
            new_part: bytes = f'${len(part)}'.encode('utf-8')
            new_parts_command.append(new_part)
            new_parts_command.append(part)

        new_parts_command.append(b'')

        return b'\r\n'.join(new_parts_command)


class RedisCache(CacheManager):
    def __init__(self, addr: Union[Tuple[str, int], str]):
        self.client = RedisClient(addr)

    def _get_data(self, key: str):
        return self.client.get_data(key)

    def _save_data(self, data, key: str, ttl: timedelta):
        self.client.set_data(key, data, ttl)
