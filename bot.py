import logging
from pyrogram import Client
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "ForwarderBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="handlers")
        )

    async def start(self):
        await super().start()
        logger.info("🔥 Auto Forwarder Bot Started Successfully!")

    async def stop(self, *args):
        await super().stop()
        logger.info("🛑 Bot Stopped.")

if __name__ == "__main__":
    Bot().run()
  
