import asyncio
from telethon import events, TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from helpers import is_admin_or_sudo, mention, chunks
from storage import add_user

# track ongoing tag operations per chat
_active: set = set()

def register(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"^[/!](all|tagall)(@\w+)?$"))
    async def tagall(event):
        await _handle(client, event)

    @client.on(events.NewMessage(pattern=r"^@all$"))
    async def tagall_at(event):
        await _handle(client, event)

async def _handle(client: TelegramClient, event):
    if event.is_private:
        await event.reply("This command only works in groups.")
        return

    if not await is_admin_or_sudo(client, event):
        await event.reply("⚠️ Only admins or sudo users can use this command.")
        return

    chat_id = event.chat_id
    if chat_id in _active:
        await event.reply("⏳ A tagging is already in progress. Use /cancel to stop it.")
        return

    _active.add(chat_id)

    try:
        participants = []
        offset = 0
        limit = 200

        status_msg = await event.reply("⏳ Fetching all members, please wait...")

        while True:
            if chat_id not in _active:
                break
            result = await client(GetParticipantsRequest(
                channel=await event.get_input_chat(),
                filter=ChannelParticipantsSearch(""),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not result.users:
                break
            for u in result.users:
                if not u.bot and not u.deleted:
                    name = (u.first_name or "") + (" " + u.last_name if u.last_name else "")
                    display = name.strip() or str(u.id)
                    participants.append((u.id, display))
                    add_user(u.id, display, u.username)
            if len(result.users) < limit:
                break
            offset += len(result.users)
            await asyncio.sleep(0.3)

        try:
            await status_msg.delete()
        except Exception:
            pass

        if not participants:
            await event.reply("No members found.")
            _active.discard(chat_id)
            return

        for chunk in chunks(participants, 5):
            if chat_id not in _active:
                await event.reply("❌ Tagging cancelled.")
                return
            text = " ".join(mention(uid, name) for uid, name in chunk)
            await event.reply(text, parse_mode="md")
            await asyncio.sleep(1.5)

    except Exception as e:
        await event.reply(f"❌ Error: {e}")
    finally:
        _active.discard(chat_id)

def cancel(chat_id):
    _active.discard(chat_id)
