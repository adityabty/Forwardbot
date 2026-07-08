from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from datetime import datetime

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.users = self.db.users
        self.banned_users = self.db.banned

    async def get_user(self, user_id: int):
        return await self.users.find_one({"user_id": user_id})

    async def save_user(self, user_id: int, data: dict):
        data["last_active"] = datetime.utcnow()
        await self.users.update_one({"user_id": user_id}, {"$set": data}, upsert=True)

    async def update_status(self, user_id: int, status: bool):
        await self.users.update_one({"user_id": user_id}, {"$set": {"forward_status": status}})

    async def remove_user(self, user_id: int):
        await self.users.delete_one({"user_id": user_id})

    async def ban_user(self, user_id: int):
        await self.banned_users.update_one({"user_id": user_id}, {"$set": {"banned_at": datetime.utcnow()}}, upsert=True)

    async def unban_user(self, user_id: int):
        await self.banned_users.delete_one({"user_id": user_id})

    async def is_banned(self, user_id: int) -> bool:
        user = await self.banned_users.find_one({"user_id": user_id})
        return user is not None

    async def get_all_active_users(self):
        return await self.users.find({"forward_status": True}).to_list(length=None)

    async def total_users_count(self) -> int:
        return await self.users.count_documents({})

db = Database()
                        
