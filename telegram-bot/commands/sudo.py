from telethon import events, TelegramClient
from helpers import is_admin_or_sudo
from storage import add_sudo_user, remove_sudo_user, get_sudo_users

def register(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"^[/!]addsudo(@\w+)?$"))
    async def addsudo(event):
        if event.is_private:
            await event.reply("This command only works in groups.")
            return
        if not await is_admin_or_sudo(client, event):
            await event.reply("⚠️ Only admins can manage sudo users.")
            return
        reply = await event.get_reply_message()
        if not reply or not reply.sender_id:
            await event.reply("Reply to a user to grant them sudo access.")
            return
        target = await reply.get_sender()
        name = getattr(target, "first_name", None) or str(target.id)
        add_sudo_user(event.chat_id, target.id)
        await event.reply(f"✅ **{name}** has been added to sudo users in this group.")

    @client.on(events.NewMessage(pattern=r"^[/!]desudo(@\w+)?$"))
    async def desudo(event):
        if event.is_private:
            await event.reply("This command only works in groups.")
            return
        if not await is_admin_or_sudo(client, event):
            await event.reply("⚠️ Only admins can manage sudo users.")
            return
        reply = await event.get_reply_message()
        if not reply or not reply.sender_id:
            await event.reply("Reply to a user to remove their sudo access.")
            return
        target = await reply.get_sender()
        name = getattr(target, "first_name", None) or str(target.id)
        remove_sudo_user(event.chat_id, target.id)
        await event.reply(f"✅ **{name}** has been removed from sudo users in this group.")

    @client.on(events.NewMessage(pattern=r"^[/!]sudolist(@\w+)?$"))
    async def sudolist(event):
        if event.is_private:
            await event.reply("This command only works in groups.")
            return
        sudos = get_sudo_users(event.chat_id)
        if not sudos:
            await event.reply("No sudo users in this group.")
            return
        lines = "\n".join(f"{i+1}. `{uid}`" for i, uid in enumerate(sudos))
        await event.reply(f"**Sudo Users:**\n{lines}", parse_mode="md")
