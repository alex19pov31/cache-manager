import hashlib
import pickle
from abc import ABC, abstractmethod
from datetime import timedelta
import socket
from typing import Callable, Tuple, Union


class CacheManager(ABC):

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


class BaseClient(ABC):
    def __init__(self, addr: Union[Tuple[str, int], str], timeout: int = 1):
        self.addr: Tuple[str, int] = addr
        self.timeout: int = timeout
        self.socket: socket.socket = None

    def __init_unix_socket(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect(self.addr)

    def __init_inet_socket(self):
        host, port = self.addr
        error = None
        info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        for family, socktype, proto, _, sockaddr in info:
            try:
                self.socket = socket.socket(family, socktype, proto)
            except Exception as e:
                error = e
                if self.socket is not None:
                    self.socket.close()
                    self.socket = None
            else:
                break
        if error is not None:
            raise error

        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(self.timeout)
        self.socket.connect(self.addr)

    def _connect(self):
        self._close()
        if isinstance(self.addr, str):
            self.__init_unix_socket()
        elif isinstance(self.addr, tuple):
            self.__init_inet_socket()

    def _close(self):
        if isinstance(self.socket, socket.socket):
            try:
                self.socket.close()
            except Exception:
                pass
        self.socket = None

    def _send_command(self, command: bytes, check_connect: bool = True) -> bytes:
        if not self.socket and check_connect:
            self._connect()

        self.socket.sendall(command)
        chunks: list = []
        while True:
            try:
                buf = self.socket.recv(1024)
                chunks.append(buf)

                if not buf or buf[-2:] == b'\r\n':
                    break
            except Exception as e:
                self._close()
                raise e

        if not len(chunks):
            return b''

        return b''.join(chunks)
