import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "forwarder_bot")
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "32_bytes_long_secret_key_here___").encode()
    SOURCE_CHAT_ID = int(os.getenv("SOURCE_CHAT_ID", "0"))
  
