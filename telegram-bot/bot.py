import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from storage import add_user, add_group
from commands.forcejoin import check_membership, force_join_text, FORCE_JOIN_CHATS

import commands.tagall as tagall
import commands.tagadmin as tagadmin
import commands.cancel as cancel
import commands.sudo as sudo
import commands.broadcast as broadcast
import commands.funtag as funtag

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER_ID = int(os.environ.get("BOT_OWNER_ID", "0"))

SESSION_PATH = os.path.join(os.path.dirname(__file__), "data", "bot_session")

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)


@client.on(events.NewMessage)
async def track_users(event):
    if event.sender_id:
        sender = await event.get_sender()
        if sender:
            name = (getattr(sender, "first_name", None) or str(sender.id))
            username = getattr(sender, "username", None)
            add_user(sender.id, name, username)
    if event.chat_id and not event.is_private:
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or str(event.chat_id)
        username = getattr(chat, "username", None)
        add_group(event.chat_id, title, username)


START_IMAGE = os.path.join(os.path.dirname(__file__), "data", "start_image.png")

ADD_ME_URL    = "https://t.me/devilxmention_bot?startgroup=start"
SUPPORT_URL   = "https://t.me/devilbotsupport"
CHANNEL_URL   = "https://t.me/devilbots971"
DEVELOPER_URL = "http://t.me/mrdevil12"

START_BUTTONS = [
    [Button.url("➕ ADD ME", ADD_ME_URL)],
    [Button.url("🛠 SUPPORT", SUPPORT_URL), Button.url("📢 CHANNEL", CHANNEL_URL)],
    [Button.url("👨‍💻 DEVELOPER", DEVELOPER_URL)],
    [Button.inline("❓ HELP", data="help")],
]


def _force_join_buttons(not_joined: list, action: str) -> list:
    """Build join buttons + a verify button for the given pending action."""
    buttons = []
    for _username, label, link in not_joined:
        buttons.append([Button.url(label, link)])
    buttons.append([Button.inline("✅ I've Joined — Continue", data=f"check_join:{action}")])
    return buttons


def build_start_caption(user_id: int, user_name: str, bot_name: str) -> str:
    return (
        f'👋 Hey <a href="tg://user?id={user_id}">{user_name}</a> !\n\n'
        f"⚡ Welcome to <b>{bot_name}</b>\n\n"
        "The ultimate Telegram Mention &amp; Tagging Bot 🚀\n"
        "━━━━━━━━━━━━━━━\n"
        "📢 <b>What can I do?</b>\n\n"
        "👥 Mention All Members\n"
        "🛡 Mention Only Admins\n"
        "📣 Send Group Notifications\n"
        "⚡ Smart &amp; Fast Tagging\n"
        "🚀 Smooth Performance\n"
        "━━━━━━━━━━━━━━━\n"
        "🔥 <b>Bot Features:</b>\n\n"
        "🔔 Tag All Members Instantly\n"
        "👑 Mention All Admins\n"
        "📌 Admin Control Commands\n"
        "⚡ Ultra Fast Mentioning\n"
        "🛡 Anti Flood Protection\n"
        "🔕 Silent Mention Support\n"
        "🎯 Custom Tag Messages\n"
        "💫 Clean &amp; Modern UI\n"
        "━━━━━━━━━━━━━━━\n"
        "💡 Add me to your group and start tagging like a pro 😎\n\n"
        "👇 <b>Choose an option below to continue.</b>"
    )


@client.on(events.NewMessage(pattern=r"^[/!]start(@\w+)?(\s+\w+)?$"))
async def start(event):
    sender    = await event.get_sender()
    user_id   = sender.id
    user_name = sender.first_name or sender.username or "User"
    bot_me    = await client.get_me()
    bot_name  = bot_me.first_name or "Devil X Mention"

    # Extract deep-link parameter (e.g. /start help)
    param = (event.pattern_match.group(2) or "").strip()

    # ── PM with ?start=help deep link → check join then send help ──
    if event.is_private and param == "help":
        if user_id != OWNER_ID:
            not_joined = await check_membership(client, user_id)
            if not_joined:
                await event.reply(
                    force_join_text(not_joined),
                    parse_mode="html",
                    buttons=_force_join_buttons(not_joined, "help"),
                )
                return
        await event.reply(build_help_text(sender.id), parse_mode="html")
        return

    # ── Group start → image + buttons only, no caption ──────
    if not event.is_private:
        if os.path.exists(START_IMAGE):
            await client.send_file(
                event.chat_id,
                START_IMAGE,
                buttons=START_BUTTONS,
            )
        else:
            await event.reply("⚡ Devil X Mention Bot", buttons=START_BUTTONS)
        return

    # ── PM start → force join check first ───────────────────
    if user_id != OWNER_ID:
        not_joined = await check_membership(client, user_id)
        if not_joined:
            await event.reply(
                force_join_text(not_joined),
                parse_mode="html",
                buttons=_force_join_buttons(not_joined, "start"),
            )
            return

    # ── PM start → all joined, show welcome ─────────────────
    caption = build_start_caption(user_id, user_name, bot_name)
    if os.path.exists(START_IMAGE):
        await client.send_file(
            event.chat_id,
            START_IMAGE,
            caption=caption,
            parse_mode="html",
            buttons=START_BUTTONS,
        )
    else:
        await event.reply(caption, parse_mode="html", buttons=START_BUTTONS)



def build_help_text(sender_id: int) -> str:
    base = (
        "📖 <b>Devil X Mention Bot — Help</b>\n"
        "━━━━━━━━━━━━━━━\n\n"

        "👥 <b>Tag Commands</b> <i>(admins/sudo only)</i>\n\n"
        "🔹 /all or /tagall — Tag all members\n"
        "🔹 @all — Also triggers tag all\n"
        "🔹 /admin or /tagadmin — Tag all admins\n"
        "🔹 /cancel — Stop an ongoing tagging\n\n"

        "━━━━━━━━━━━━━━━\n"
        "🎉 <b>Fun Tag Commands</b> <i>(admins/sudo only)</i>\n\n"
        "🌙 /gntag — Tag all with Good Night messages\n"
        "☀️ /gmtag — Tag all with Good Morning messages\n"
        "👋 /hitag — Tag all with Hi/Hello messages\n"
        "💭 /lifetag — Tag all with life quotes\n"
        "🌹 /shayari — Tag all with shayari\n\n"
        "🛑 <b>Stop Fun Tags:</b>\n"
        "• /gnstop • /gmstop • /histop\n"
        "• /lifestop • /shayarioff\n\n"

        "━━━━━━━━━━━━━━━\n"
        "🔑 <b>Sudo Management</b> <i>(admins only)</i>\n\n"
        "🔸 /addsudo — Reply to user to grant sudo\n"
        "🔸 /desudo — Reply to user to revoke sudo\n"
        "🔸 /sudolist — List sudo users in this group\n\n"

        "━━━━━━━━━━━━━━━\n"
        "💡 <b>Tip:</b> Make the bot <b>admin</b> in your group to tag all members!"
    )
    if sender_id == OWNER_ID:
        base += (
            "\n\n━━━━━━━━━━━━━━━\n"
            "👑 <b>Owner Only</b>\n\n"
            "🔺 /broadcast &lt;msg&gt; — Send to all users\n"
            "🔺 /users — List all known groups &amp; users"
        )
    return base


# /help command
@client.on(events.NewMessage(pattern=r"^[/!]help(@\w+)?$"))
async def help_cmd(event):
    sender = await event.get_sender()

    # ── In a group → send a button that opens PM and auto-triggers /help ──
    if not event.is_private:
        bot_me = await client.get_me()
        bot_username = bot_me.username
        await event.reply(
            "📖 Click below to get help in my PM:",
            buttons=[[Button.url("📖 GET HELP", f"https://t.me/{bot_username}?start=help")]],
        )
        return

    # ── In PM → send full help text ──
    await event.reply(build_help_text(sender.id), parse_mode="html")


# HELP button clicked
@client.on(events.CallbackQuery(data=b"help"))
async def help_callback(event):
    await event.answer()
    sender = await event.get_sender()

    # ── In a group → show redirect button to PM ──────────────
    if not event.is_private:
        bot_me = await client.get_me()
        bot_username = bot_me.username
        await event.edit(
            "📖 Click below to get help in my PM:",
            buttons=[[Button.url("📖 GET HELP", f"https://t.me/{bot_username}?start=help")]],
        )
        return

    # ── In PM → show full help text + BACK button ────────────
    await event.edit(
        build_help_text(sender.id),
        parse_mode="html",
        buttons=[[Button.inline("🔙 BACK", data="back_start")]],
    )


# Force join verification button clicked
@client.on(events.CallbackQuery(pattern=b"check_join:.*"))
async def check_join_callback(event):
    await event.answer()
    sender = await event.get_sender()
    user_id = sender.id
    action = event.data.decode().split(":", 1)[1]

    not_joined = await check_membership(client, user_id)
    if not_joined:
        await event.answer("❌ You haven't joined yet! Please join and try again.", alert=True)
        await event.edit(
            force_join_text(not_joined),
            parse_mode="html",
            buttons=_force_join_buttons(not_joined, action),
        )
        return

    # All joined — proceed with the pending action
    user_name = sender.first_name or sender.username or "User"
    bot_me = await client.get_me()
    bot_name = bot_me.first_name or "Devil X Mention"

    if action == "help":
        await event.edit(build_help_text(user_id), parse_mode="html")
    else:
        # Default: show welcome screen
        caption = build_start_caption(user_id, user_name, bot_name)
        if os.path.exists(START_IMAGE):
            await event.delete()
            await client.send_file(
                event.chat_id,
                START_IMAGE,
                caption=caption,
                parse_mode="html",
                buttons=START_BUTTONS,
            )
        else:
            await event.edit(caption, parse_mode="html", buttons=START_BUTTONS)


# BACK button clicked — edit message back to start screen
@client.on(events.CallbackQuery(data=b"back_start"))
async def back_callback(event):
    await event.answer()
    sender = await event.get_sender()
    user_id   = sender.id
    user_name = sender.first_name or sender.username or "User"
    bot_me    = await client.get_me()
    bot_name  = bot_me.first_name or "Devil X Mention"

    caption = build_start_caption(user_id, user_name, bot_name)
    await event.edit(caption, parse_mode="html", buttons=START_BUTTONS)


def main():
    print("Starting Devil X Mention Bot...")

    tagall.register(client)
    tagadmin.register(client)
    cancel.register(client)
    sudo.register(client)
    broadcast.register(client)
    funtag.register(client)

    client.start(bot_token=BOT_TOKEN)
    print(f"Bot started successfully! Owner ID: {OWNER_ID}")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
