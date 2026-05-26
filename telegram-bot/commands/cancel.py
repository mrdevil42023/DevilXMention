from telethon import events, TelegramClient
from helpers import is_admin_or_sudo
import commands.tagall as tagall_mod
import commands.tagadmin as tagadmin_mod

def register(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"^[/!]cancel(@\w+)?$"))
    async def cancel(event):
        if event.is_private:
            await event.reply("This command only works in groups.")
            return

        if not await is_admin_or_sudo(client, event):
            await event.reply("⚠️ Only admins or sudo users can cancel tagging.")
            return

        chat_id = event.chat_id
        tagall_mod.cancel(chat_id)
        tagadmin_mod.cancel(chat_id)
        await event.reply("✅ Tagging cancelled.")
