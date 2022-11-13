from redis import Redis

# Dependency
def get_cache():
    db = Redis(host='127.0.0.1', port=6379,password='wasionsime')
    try:
        yield db
    finally:
        db.close()