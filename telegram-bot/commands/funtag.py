import asyncio
import random
from telethon import events, TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import FloodWaitError
from helpers import is_admin_or_sudo
from commands.funtag_messages import (
    GM_MESSAGES,
    GN_MESSAGES,
    HI_MESSAGES,
    QUOTES,
    SHAYARI,
    TAG_ALL,
)

spam_chats: set = set()
active_tags: dict = {}


async def mention_members(client: TelegramClient, event, message_pool: list, stop_cmd: str):
    if event.is_private:
        await event.reply("❗ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘs.")
        return

    if not await is_admin_or_sudo(client, event):
        await event.reply("🚫 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴏʀ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return

    chat_id = event.chat_id

    if chat_id in spam_chats:
        stop_command = active_tags.get(chat_id, stop_cmd)
        await event.reply(
            f"⚠️ ᴀ ᴛᴀɢɢɪɴɢ sᴇssɪᴏɴ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ.\n"
            f"➤ ᴜsᴇ /{stop_command} ᴛᴏ sᴛᴏᴘ ɪᴛ."
        )
        return

    spam_chats.add(chat_id)
    active_tags[chat_id] = stop_cmd

    try:
        offset = 0
        limit = 200
        while True:
            if chat_id not in spam_chats:
                break
            result = await client(GetParticipantsRequest(
                channel=await event.get_input_chat(),
                filter=ChannelParticipantsSearch(""),
                offset=offset,
                limit=limit,
                hash=0,
            ))
            if not result.users:
                break
            for user in result.users:
                if chat_id not in spam_chats:
                    break
                if user.bot or user.deleted:
                    continue
                name = (user.first_name or "") + (" " + user.last_name if user.last_name else "")
                name = name.strip() or str(user.id)
                try:
                    msg = random.choice(message_pool)
                    await client.send_message(
                        chat_id,
                        f"[{name}](tg://user?id={user.id}) {msg}",
                        parse_mode="md",
                    )
                    await asyncio.sleep(4)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print(f"Error tagging user: {e}")
                    continue
            if len(result.users) < limit:
                break
            offset += len(result.users)
    finally:
        spam_chats.discard(chat_id)
        active_tags.pop(chat_id, None)
        if chat_id in spam_chats or True:
            try:
                await client.send_message(chat_id, "✅ ᴛᴀɢɢɪɴɢ sᴇssɪᴏɴ ᴇɴᴅᴇᴅ.")
            except Exception:
                pass


def register(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"^[/!]gntag(@\w+)?$"))
    async def gntag(event):
        await mention_members(client, event, GN_MESSAGES, "gnstop")

    @client.on(events.NewMessage(pattern=r"^[/!]gmtag(@\w+)?$"))
    async def gmtag(event):
        await mention_members(client, event, GM_MESSAGES, "gmstop")

    @client.on(events.NewMessage(pattern=r"^[/!]hitag(@\w+)?$"))
    async def hitag(event):
        await mention_members(client, event, HI_MESSAGES, "histop")

    @client.on(events.NewMessage(pattern=r"^[/!]lifetag(@\w+)?$"))
    async def lifetag(event):
        await mention_members(client, event, QUOTES, "lifestop")

    @client.on(events.NewMessage(pattern=r"^[/!]shayari(@\w+)?$"))
    async def shayari_tag(event):
        await mention_members(client, event, SHAYARI, "shayarioff")

    @client.on(events.NewMessage(pattern=r"^[/!](gnstop|gmstop|histop|lifestop|shayarioff|tagoff|tagstop)(@\w+)?$"))
    async def stop_tagging(event):
        if event.is_private:
            return
        if not await is_admin_or_sudo(client, event):
            await event.reply("🚫 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴛᴏᴘ ᴛᴀɢɢɪɴɢ.")
            return
        chat_id = event.chat_id
        if chat_id not in spam_chats:
            await event.reply("⚠️ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴛᴀɢɢɪɴɢ sᴇssɪᴏɴ ғᴏᴜɴᴅ.")
            return
        spam_chats.discard(chat_id)
        active_tags.pop(chat_id, None)
        await event.reply("✅ ᴍᴇɴᴛɪᴏɴɪɴɢ sᴛᴏᴘᴘᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
