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

cache_manager = MemcachedCache(('10.5.0.11', 11211))

@cache_manager(ttl=timedelta(hours=1))
def some_function():
    pass
    
```

Redis:
```python
from cache_manager.redis import RedisCache
from datetime import timedelta

cache_manager = RedisCache(('10.5.0.11', 6379), password='somepassword')

@cache_manager(ttl=timedelta(hours=1))
def some_function():
    pass
    
```

