import redis

redis_client = redis.Redis(
  host="localhost",
  port=6379,
  db=0,
  protocol=2,
  decode_responses=True
)