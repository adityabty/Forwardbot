from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database.mongo import db

@Client.on_message(filters.command("stats") & filters.user(Config.ADMIN_IDS))
async def admin_stats(client: Client, message: Message):
    total = await db.total_users_count()
    active_users = await db.get_all_active_users()
    await message.reply(f"📊 **System Statistics**\n\nTotal Registered Users: {total}\nActive Sessions running: {len(active_users)}")

@Client.on_message(filters.command("ban") & filters.user(Config.ADMIN_IDS))
async def ban_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/ban user_id`")
    target_id = int(message.command[1])
    await db.ban_user(target_id)
    await db.remove_user(target_id)
    await message.reply(f"🔨 User `{target_id}` has been banned and session deleted.")

@Client.on_message(filters.command("unban") & filters.user(Config.ADMIN_IDS))
async def unban_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/unban user_id`")
    target_id = int(message.command[1])
    await db.unban_user(target_id)
    await message.reply(f"✅ User `{target_id}` has been unbanned.")
  
