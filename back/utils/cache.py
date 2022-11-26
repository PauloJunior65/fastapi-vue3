from .config import get_settings
import pickle
import redis

settings = get_settings()

# Dependency
class CacheCustom:
    def __init__(self):
        pass

    def __call__(self, **kwars):
        db = RedisCache(**kwars)
        try:
            yield db
        finally:
            db._cache.close()

# Dependency
def get_cache():
    db = RedisCache()
    try:
        yield db
    finally:
        db._cache.close()
        
class RedisSerializer:
    """
    Similar to PickSerializer, except integers are serialized as native Redis
    integers for better incr() and decr() atomicity.
    """
    def __init__(self, protocol=None):
        self.protocol = pickle.HIGHEST_PROTOCOL if protocol is None else protocol

    def dumps(self, obj):
        # Only skip pickling for integers, a int subclasses as bool should be
        # pickled.
        if type(obj) is int:
            return obj
        return pickle.dumps(obj, self.protocol)

    def loads(self, data):
        try:
            return int(data)
        except ValueError:
            return pickle.loads(data)
        
class RedisCache:
    _cache:redis.Redis
    def __init__(self,**kwars):
        con = settings.redis()
        con.update(kwars)
        self._cache = redis.Redis(**con)
        self._serializer = RedisSerializer()

    def add(self, key:str, value, timeout = settings.REDIS_TIMEOUT):
        value = self._serializer.dumps(value)
        return bool(self._cache.set(key, value, ex=timeout, nx=True))

    def get(self, key:str, default = None):
        value = self._cache.get(key)
        return default if value is None else self._serializer.loads(value)

    def set(self, key, value, timeout = settings.REDIS_TIMEOUT):
        value = self._serializer.dumps(value)
        self._cache.set(key, value, ex=timeout)

    def touch(self, key, timeout = settings.REDIS_TIMEOUT):
        if timeout is None:
            return bool(self._cache.persist(key))
        else:
            return bool(self._cache.expire(key, timeout))

    def delete(self, key):
        return bool(self._cache.delete(key))

    def get_many(self, keys):
        ret = self._cache.mget(keys)
        return {
            k: self._serializer.loads(v) for k, v in zip(keys, ret) if v is not None
        }

    def has_key(self, key):
        return bool(self._cache.exists(key))

    def incr(self, key, delta):
        if not self._cache.exists(key):
            raise ValueError("Key '%s' not found." % key)
        return self._cache.incr(key, delta)

    def set_many(self, data, timeout = settings.REDIS_TIMEOUT):
        pipeline = self._cache.pipeline()
        pipeline.mset({k: self._serializer.dumps(v) for k, v in data.items()})
        if timeout is not None:
            # Setting timeout for each key as redis does not support timeout
            # with mset().
            for key in data:
                pipeline.expire(key, timeout)
        pipeline.execute()

    def delete_many(self, keys):
        self._cache.delete(*keys)

    def clear(self):
        return bool(self._cache.flushdb())
