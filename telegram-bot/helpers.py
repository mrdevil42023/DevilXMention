import asyncio
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from storage import get_sudo_users

async def is_admin_or_sudo(client: TelegramClient, event) -> bool:
    chat_id = event.chat_id
    sender_id = event.sender_id
    sudo_list = get_sudo_users(chat_id)
    if str(sender_id) in sudo_list:
        return True
    try:
        perms = await client.get_permissions(chat_id, sender_id)
        return perms.is_admin or perms.is_creator
    except Exception:
        return False

def mention(user_id: int, name: str) -> str:
    safe = name.replace("[", "").replace("]", "")
    return f"[{safe}](tg://user?id={user_id})"

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
