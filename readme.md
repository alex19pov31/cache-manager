# Cache manager

Простой кеш - хранение в файлах:

```python
from cache_manager.pickle import PickleCache
from datetime import timedelta

cache_manager = PickleCache('./cache')

@cache_manager(ttl=timedelta(hours=1))
def some_function():
    pass
    
```

Memcached:
```python
from cache_manager.memcached import MemcachedCache
from datetime import timedelta

cache_manager = MemcachedCache(('10.5.0.11', 11211)) # в случае соединения по TCP или UDP сокету
cache_manager = MemcachedCache('/usr/run/memcached.sock') # в случае соединия по unix сокету

@cache_manager(ttl=timedelta(hours=1))
def some_function():
    pass
    
```

Redis:
```python
from cache_manager.redis import RedisCache
from datetime import timedelta

cache_manager = RedisCache(('10.5.0.11', 6379), password='somepassword') # в случае соединения по TCP или UDP сокету
cache_manager = RedisCache('/usr/run/redis.sock', password='somepassword') # в случае соединия по unix сокету

@cache_manager(ttl=timedelta(hours=1))
def some_function():
    pass
    
```


Etcd:
```python
from cache_manager.etcd import EtcdCache
from datetime import timedelta

cache_manager = EtcdCache(('10.5.0.11', 2371), scheme='http')

@cache_manager(ttl=timedelta(hours=1))
def some_function():
    pass
    
```

