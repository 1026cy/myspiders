import redis
myredis=redis.Redis(host="127.0.0.1",port=6379)
url="https://baike.baidu.com/item/Python/407313"
myredis.lpush("baike_redis:start_urls",url)
