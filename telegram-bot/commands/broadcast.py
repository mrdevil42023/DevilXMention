import os
from telethon import events, TelegramClient
from storage import get_users, get_groups

OWNER_ID = int(os.environ.get("BOT_OWNER_ID", "0"))


def register(client: TelegramClient):

    @client.on(events.NewMessage(pattern=r"^[/!]broadcast(.*)$"))
    async def broadcast(event):
        if event.sender_id != OWNER_ID:
            await event.reply("⛔ This command is only for the bot owner.")
            return

        text = event.pattern_match.group(1).strip()
        if not text:
            await event.reply("Usage: /broadcast <message>")
            return

        users = get_users()
        total = len(users)
        sent = 0
        failed = 0

        status = await event.reply(f"📢 Broadcasting to {total} users...")

        for row in users:
            try:
                await client.send_message(int(row["user_id"]), text)
                sent += 1
            except Exception:
                failed += 1

        await status.delete()
        await event.reply(
            f"✅ Broadcast complete.\nSent: **{sent}** | Failed: **{failed}**",
            parse_mode="md"
        )

    @client.on(events.NewMessage(pattern=r"^[/!]users(@\w+)?$"))
    async def users_cmd(event):
        if event.sender_id != OWNER_ID:
            await event.reply("⛔ This command is only for the bot owner.")
            return

        groups = get_groups()
        users = get_users()

        # ── Groups section ──────────────────────────────
        if groups:
            group_lines = []
            for row in groups:
                if row.get("username"):
                    group_lines.append(f"• {row['title']} [t.me/{row['username']}]")
                else:
                    group_lines.append(f"• {row['title']}")
            groups_text = f"👥 **Groups** ({len(groups)})\n" + "\n".join(group_lines)
        else:
            groups_text = "👥 **Groups**\n_None yet._"

        # ── Users section ───────────────────────────────
        if users:
            user_lines = []
            for row in users:
                if row.get("username"):
                    user_lines.append(f"• {row['name']} [@{row['username']}]")
                else:
                    user_lines.append(f"• {row['name']}")
            users_text = f"🙋 **Users** ({len(users)})\n" + "\n".join(user_lines)
        else:
            users_text = "🙋 **Users**\n_None yet._"

        await event.reply(
            f"{groups_text}\n\n{users_text}",
            parse_mode="md"
        )
