from upstash_redis import Redis

from api.config import Config

redis = Redis(
    url=Config.UPSTASH_URL,
    token=Config.UPSTASH_TOKEN
)
