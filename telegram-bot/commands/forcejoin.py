from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError, ChannelPrivateError

# Chats the user must join before using the bot
FORCE_JOIN_CHATS = [
    ("devilbots971",    "📢 Channel",       "https://t.me/devilbots971"),
    ("devilbotsupport", "💬 Support Group", "https://t.me/devilbotsupport"),
]


async def check_membership(client: TelegramClient, user_id: int) -> list:
    """
    Returns list of (username, label, link) for chats the user has NOT joined.
    Empty list means the user has joined all required chats.
    """
    not_joined = []
    for username, label, link in FORCE_JOIN_CHATS:
        try:
            result = await client(GetParticipantRequest(channel=username, participant=user_id))
            from telethon.tl.types import ChannelParticipantBanned, ChannelParticipantLeft
            if isinstance(result.participant, (ChannelParticipantBanned, ChannelParticipantLeft)):
                not_joined.append((username, label, link))
        except UserNotParticipantError:
            not_joined.append((username, label, link))
        except (ChatAdminRequiredError, ChannelPrivateError, Exception):
            # If we can't check (bot not in chat, private, etc.) — don't block the user
            pass
    return not_joined


def force_join_text(not_joined: list) -> str:
    lines = [
        "⚠️ <b>Access Restricted!</b>\n",
        "You must join our official channels before using the bot.\n",
    ]
    for _username, label, link in not_joined:
        lines.append(f"👉 {label}: {link}")
    lines.append("\n✅ After joining, tap <b>I've Joined</b> to continue.")
    return "\n".join(lines)
