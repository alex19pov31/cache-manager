import json
from http.client import HTTPResponse
from datetime import timedelta
from typing import Tuple
from urllib import request
from cache_manager.base import CacheManager


class EtcdClient:
    def __init__(self, addr: Tuple[str, int], scheme: str = 'http'):
        self.addr: Tuple[str, int] = addr
        self.scheme: str = scheme

    def __get_base_url(self) -> str:
        host, port = self.addr
        return f'{self.scheme}://{host}:{port}/v2'

    def __send_request(self, action: str, data=None, method: str = 'POST') -> HTTPResponse:
        url: str = f'{self.__get_base_url()}/{action}'
        req = request.Request(url, data=data, method=method)
        return request.urlopen(req)

    def set_data(self, key: str, value, expire: timedelta) -> bool:
        resp: HTTPResponse = self.__send_request(f'keys/{key}', {
            'value': value,
            'ttl': expire.seconds
        }, method='PUT')
        return resp.getcode() == 200

    def get_data(self, key: str):
        resp: HTTPResponse = self.__send_request(f'keys/{key}', method='GET')
        result: str = resp.read().decode('utf-8')
        if not result:
            return None

        json_data: dict = json.loads(result)
        node: dict = json_data.get('node')
        if not node:
            return None

        return node.get('value')


class EtcdCache(CacheManager):
    def __init__(self, addr: Tuple[str, int], scheme: str = 'http'):
        self.client = EtcdClient(addr, scheme)

    def _get_data(self, key: str):
        return self.client.get_data(key)

    def _save_data(self, data, key: str, ttl: timedelta):
        self.client.set_data(key, data, ttl)

