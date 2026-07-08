from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.mongo import db
from utils.encryption import encrypt_session
from utils.helpers import validate_and_get_groups
from config import Config
from datetime import datetime

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Login (Session)", callback_data="login"), InlineKeyboardButton("👤 My Account", callback_data="account")],
        [InlineKeyboardButton("📊 Total Groups", callback_data="groups"), InlineKeyboardButton("🔄 Status: Toggle", callback_data="toggle_status")],
        [InlineKeyboardButton("🚪 Logout", callback_data="logout"), InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ])

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    if await db.is_banned(message.from_user.id):
        return await message.reply("❌ You are banned from using this bot.")
    
    await message.reply_text(
        "👋 **Welcome to the Premium Auto Forwarder Bot**\n\nManage your automated delivery campaigns securely via user sessions.",
        reply_markup=get_main_menu()
    )

@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if await db.is_banned(user_id):
        return await query.answer("You are banned.", show_alert=True)

    data = query.data
    user_data = await db.get_user(user_id)

    if data == "account":
        if not user_data:
            return await query.answer("❌ You are not logged in!", show_alert=True)
        text = (
            f"👤 **Account Information**\n\n"
            f"**Name:** {user_data['name']}\n"
            f"**Username:** @{user_data['username']}\n"
            f"**User ID:** `{user_data['user_id']}`\n"
            f"**Status:** {'🟢 Active' if user_data['forward_status'] else '🔴 Inactive'}"
        )
        await query.message.edit_text(text, reply_markup=get_main_menu())

    elif data == "groups":
        if not user_data:
            return await query.answer("❌ You are not logged in!", show_alert=True)
        await query.answer(f"📋 Total accessible groups: {user_data['group_count']}", show_alert=True)

    elif data == "toggle_status":
        if not user_data:
            return await query.answer("❌ You are not logged in!", show_alert=True)
        new_status = not user_data["forward_status"]
        await db.update_status(user_id, new_status)
        await query.answer(f"Status changed to {'ON' if new_status else 'OFF'}", show_alert=True)

    elif data == "logout":
        if not user_data:
            return await query.answer("❌ You are not logged in!", show_alert=True)
        await db.remove_user(user_id)
        await query.answer("🚪 Logged out successfully.", show_alert=True)
        await query.message.edit_text("🚪 Logged out. Send /start to connect again.", reply_markup=None)

    elif data == "help":
        await query.message.edit_text("ℹ️ **Help & Guide**\n\n1. Generate a Pyrogram string session.\n2. Click login and follow instructions.\n3. Turn Status ON.\n4. Every new message in the source channel will be broadcasted to your groups.", reply_markup=get_main_menu())

    elif data == "login":
        await query.message.reply_text("📥 Please send your Pyrogram **String Session** directly as a text message.")
        await query.answer()

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "broadcast"]))
async def handle_session_input(client: Client, message: Message):
    if await db.is_banned(message.from_user.id): return
    
    # Check if input looks like a potential session string
    if len(message.text) < 50:
        return

    status_msg = await message.reply("⏳ Validating session... please wait.")
    res = await validate_and_get_groups(message.text, Config.API_ID, Config.API_HASH)
    
    if not res["valid"]:
        return await status_msg.edit("❌ **Invalid String Session.** Check credentials and try again.")
    
    encrypted = encrypt_session(message.text)
    user_payload = {
        "user_id": message.from_user.id,
        "session": encrypted,
        "name": res["name"],
        "username": res["username"],
        "group_count": res["group_count"],
        "forward_status": True,
        "join_date": datetime.utcnow()
    }
    await db.save_user(message.from_user.id, user_payload)
    await status_msg.edit(f"✅ **Login Successful!**\n\n👤 **Name:** {res['name']}\n👥 **Groups Detected:** {res['group_count']}")
      
