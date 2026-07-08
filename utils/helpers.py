from pyrogram import Client
import logging

logger = logging.getLogger(__name__)

async def validate_and_get_groups(session_string: str, api_id: int, api_hash: int):
    try:
        async with Client("temp_session", api_id=api_id, api_hash=api_hash, session_string=session_string, in_memory=True) as app:
            me = await app.get_me()
            groups_count = 0
            async for dialog in app.get_dialogs():
                if dialog.chat.type in ["group", "supergroup"]:
                    groups_count += 1
            return {
                "valid": True,
                "name": f"{me.first_name or ''} {me.last_name or ''}".strip(),
                "username": me.username or "N/A",
                "id": me.id,
                "group_count": groups_count
            }
    except Exception as e:
        logger.error(f"Session validation failed: {e}")
        return {"valid": False}
      
