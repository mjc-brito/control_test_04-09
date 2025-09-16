import os
import redis

#DB 2 so para a fila
QUEUE_REDIS_URL = os.environ.get('QUEUE_REDIS_URL', 'redis://127.0.0.1:6379/2')
r = redis.Redis.from_url(QUEUE_REDIS_URL, decode_responses=True)
QUEUE_KEY = 'fila:users'

def get_queue():
    return r.lrange(QUEUE_KEY, 0, -1)

def get_first():
    return r.lindex(QUEUE_KEY, 0)

def add_to_queue(username: str):
    if r.lpos(QUEUE_KEY, username) is None:
        r.rpush(QUEUE_KEY, username)

def remove_from_queue(username: str):
    r.lrem(QUEUE_KEY, 0, username)

def clear_queue():
    r.delete(QUEUE_KEY)