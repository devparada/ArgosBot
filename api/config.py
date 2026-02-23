import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Variables
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    MY_USER_ID = os.environ.get("MY_USER_ID", "")
    TARGET_URL = os.environ.get("TARGET_URL", "").replace("https://", "").replace("http://", "")

    # Upstash Redis
    UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
    UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")

    # Security
    SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "")
