from upstash_redis import Redis

from api.config.config import Config

redis = Redis(
    url=Config.UPSTASH_URL,
    token=Config.UPSTASH_TOKEN
)
