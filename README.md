# 🤖 DevilXMention Bot

<p align="center">
  <b>The ultimate Telegram Mention & Tagging Bot</b><br>
  Tag all members or admins in a group instantly — with sudo management, fun tags, force join, and owner broadcast tools.
</p>

<p align="center">
  <a href="https://t.me/devilxmention_bot"><img src="https://img.shields.io/badge/Bot-@devilxmention__bot-blue?logo=telegram" /></a>
  <a href="https://t.me/devilbotsupport"><img src="https://img.shields.io/badge/Support-Group-green?logo=telegram" /></a>
  <a href="https://t.me/devilbots971"><img src="https://img.shields.io/badge/Channel-@devilbots971-red?logo=telegram" /></a>
  <img src="https://img.shields.io/badge/Python-3.11-yellow?logo=python" />
  <img src="https://img.shields.io/badge/Telethon-MTProto-blueviolet" />
</p>

---

## ✨ Features

- 👥 **Tag All Members** — Instantly mention every member in a group
- 🛡 **Tag All Admins** — Mention only the admins
- 🎉 **Fun Tags** — Good Night, Good Morning, Hi, Life Quotes, Shayari tags
- 🔑 **Sudo Management** — Grant/revoke sudo access per group
- 📢 **Owner Broadcast** — Send a message to all known users
- 🔒 **Force Join** — Users must join your channel & support group before using the bot
- 🛑 **Anti-Flood** — Batched tagging with delays to avoid Telegram limits
- 💾 **Supabase Database** — All data persisted in the cloud

---

## 📋 Commands

### Tagging (admins / sudo users only)
| Command | Description |
|---|---|
| `/all` or `/tagall` or `@all` | Tag all members |
| `/admin` or `/tagadmin` | Tag all admins |
| `/cancel` | Stop an ongoing tagging |

### Fun Tags (admins / sudo users only)
| Command | Description |
|---|---|
| `/gntag` | Tag all with Good Night messages |
| `/gmtag` | Tag all with Good Morning messages |
| `/hitag` | Tag all with Hi/Hello messages |
| `/lifetag` | Tag all with life quotes |
| `/shayari` | Tag all with shayari |
| `/gnstop` `/gmstop` `/histop` `/lifestop` `/shayarioff` | Stop the respective fun tag |

### Sudo Management (admins only)
| Command | Description |
|---|---|
| `/addsudo` | Reply to a user to grant sudo |
| `/desudo` | Reply to a user to revoke sudo |
| `/sudolist` | List sudo users in this group |

### Owner Only
| Command | Description |
|---|---|
| `/broadcast <message>` | Send message to all known users |
| `/users` | List all groups and users |

---

## ⚙️ Prerequisites

Before hosting, you need these credentials:

| Credential | Where to get it |
|---|---|
| `TELEGRAM_API_ID` | [my.telegram.org](https://my.telegram.org) → App configuration |
| `TELEGRAM_API_HASH` | [my.telegram.org](https://my.telegram.org) → App configuration |
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) on Telegram |
| `BOT_OWNER_ID` | [@userinfobot](https://t.me/userinfobot) on Telegram |
| `SUPABASE_URL` | [supabase.com](https://supabase.com) → Project Settings → API |
| `SUPABASE_KEY` | [supabase.com](https://supabase.com) → Project Settings → API → service_role key |

### 🗄️ Supabase Table Setup

Run this SQL in your Supabase project → **SQL Editor**:

```sql
CREATE TABLE IF NOT EXISTS bot_users (
    user_id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bot_groups (
    chat_id BIGINT PRIMARY KEY,
    title TEXT NOT NULL,
    username TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sudo_users (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    PRIMARY KEY (chat_id, user_id)
);
```

---

## 🚀 Hosting Guide

---

### 📱 Termux (Android)

> Run the bot directly on your Android phone — no PC needed.

**Step 1 — Install Termux**

Download Termux from [F-Droid](https://f-droid.org/packages/com.termux/) (not Play Store).

**Step 2 — Set up the environment**

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
```

**Step 3 — Clone the bot**

```bash
git clone https://github.com/mrdevil42023/DevilXMention.git
cd DevilXMention/telegram-bot
```

**Step 4 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 5 — Set environment variables**

```bash
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export BOT_OWNER_ID="your_user_id"
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your_service_role_key"
```

> To make these permanent, add them to `~/.bashrc`:
> ```bash
> echo 'export TELEGRAM_API_ID="your_api_id"' >> ~/.bashrc
> source ~/.bashrc
> ```

**Step 6 — Run the bot**

```bash
python3 bot.py
```

> To keep it running after closing Termux, use `nohup`:
> ```bash
> nohup python3 bot.py &
> ```

---

### 🐧 Linux VPS (Ubuntu / Debian)

**Step 1 — Connect to your VPS**

```bash
ssh root@your_server_ip
```

**Step 2 — Install Python**

```bash
apt update && apt upgrade -y
apt install python3 python3-pip git -y
```

**Step 3 — Clone the bot**

```bash
git clone https://github.com/mrdevil42023/DevilXMention.git
cd DevilXMention/telegram-bot
```

**Step 4 — Install dependencies**

```bash
pip3 install -r requirements.txt
```

**Step 5 — Create environment file**

```bash
cp .env.example .env
nano .env   # fill in your values, then Ctrl+X to save
```

**Step 6 — Load env and run**

```bash
export $(grep -v '^#' .env | xargs)
python3 bot.py
```

**Step 7 — Run as a background service (systemd)**

```bash
nano /etc/systemd/system/devilxmention.service
```

Paste this (update the paths):

```ini
[Unit]
Description=DevilXMention Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/DevilXMention/telegram-bot
EnvironmentFile=/root/DevilXMention/telegram-bot/.env
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable devilxmention
systemctl start devilxmention
systemctl status devilxmention   # check it's running
```

---

### 🪟 Windows (Local)

**Step 1 — Install Python**

Download Python 3.11 from [python.org](https://www.python.org/downloads/).
During install, check ✅ **Add Python to PATH**.

**Step 2 — Clone the bot**

Open Command Prompt:

```cmd
git clone https://github.com/mrdevil42023/DevilXMention.git
cd DevilXMention\telegram-bot
```

**Step 3 — Install dependencies**

```cmd
pip install -r requirements.txt
```

**Step 4 — Set environment variables**

```cmd
set TELEGRAM_API_ID=your_api_id
set TELEGRAM_API_HASH=your_api_hash
set TELEGRAM_BOT_TOKEN=your_bot_token
set BOT_OWNER_ID=your_user_id
set SUPABASE_URL=https://your-project.supabase.co
set SUPABASE_KEY=your_service_role_key
```

**Step 5 — Run the bot**

```cmd
python bot.py
```

---

### 🐳 Docker

**Step 1 — Install Docker**

Follow the official guide: [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)

**Step 2 — Clone and enter the bot directory**

```bash
git clone https://github.com/mrdevil42023/DevilXMention.git
cd DevilXMention/telegram-bot
```

**Step 3 — Build the image**

```bash
docker build -t devilxmention .
```

**Step 4 — Run the container**

```bash
docker run -d \
  -e TELEGRAM_API_ID=your_api_id \
  -e TELEGRAM_API_HASH=your_api_hash \
  -e TELEGRAM_BOT_TOKEN=your_bot_token \
  -e BOT_OWNER_ID=your_user_id \
  -e SUPABASE_URL=https://your-project.supabase.co \
  -e SUPABASE_KEY=your_service_role_key \
  --name devilxmention \
  --restart always \
  devilxmention
```

Check logs:
```bash
docker logs -f devilxmention
```

---

### 🚄 Railway

> Free hosting with 500 hours/month on the free tier.

**Step 1** — Go to [railway.app](https://railway.app) and log in with GitHub.

**Step 2** — Click **New Project → Deploy from GitHub repo** → select your fork of this repo.

**Step 3** — Set the **Root Directory** to `telegram-bot`.

**Step 4** — Go to your project → **Variables** tab → add all 6 environment variables:

```
TELEGRAM_API_ID
TELEGRAM_API_HASH
TELEGRAM_BOT_TOKEN
BOT_OWNER_ID
SUPABASE_URL
SUPABASE_KEY
```

**Step 5** — Railway will auto-detect the `Procfile` and start the bot with `python3 bot.py`.

---

### 🎨 Render

> Free web service hosting.

**Step 1** — Go to [render.com](https://render.com) → **New → Background Worker**.

**Step 2** — Connect your GitHub repo.

**Step 3** — Set:
- **Root Directory:** `telegram-bot`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python3 bot.py`

**Step 4** — Add all 6 environment variables in the **Environment** tab.

**Step 5** — Click **Create Background Worker**.

---

### ☁️ Heroku

**Step 1 — Install Heroku CLI**

Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

**Step 2 — Login and create app**

```bash
heroku login
heroku create devilxmention-bot
```

**Step 3 — Set environment variables**

```bash
heroku config:set TELEGRAM_API_ID=your_api_id
heroku config:set TELEGRAM_API_HASH=your_api_hash
heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token
heroku config:set BOT_OWNER_ID=your_user_id
heroku config:set SUPABASE_URL=https://your-project.supabase.co
heroku config:set SUPABASE_KEY=your_service_role_key
```

**Step 4 — Deploy**

```bash
git subtree push --prefix telegram-bot heroku main
```

**Step 5 — Start the worker**

```bash
heroku ps:scale worker=1
heroku logs --tail
```

---

### 🟣 Koyeb

**Step 1** — Go to [koyeb.com](https://app.koyeb.com) and sign up.

**Step 2** — Click **Create App → GitHub** → connect your repo.

**Step 3** — Set:
- **Build type:** Dockerfile
- **Dockerfile path:** `telegram-bot/Dockerfile`

**Step 4** — Add all 6 environment variables.

**Step 5** — Deploy.

---

### ♻️ Replit

**Step 1** — Go to [replit.com](https://replit.com) → **Import from GitHub** → paste this repo URL.

**Step 2** — Open **Secrets** (🔒 icon) and add all 6 environment variables.

**Step 3** — Run the Supabase SQL (see Prerequisites above).

**Step 4** — Click **Run** — the bot starts automatically.

> To keep it alive 24/7, enable **Always On** (requires Replit Core plan) or use [UptimeRobot](https://uptimerobot.com) to ping your Repl.

---

## 📁 Project Structure

```
telegram-bot/
├── bot.py                  # Main entry point
├── storage.py              # Supabase database layer
├── helpers.py              # Shared utilities
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker deployment
├── Procfile                # Heroku / Railway
├── runtime.txt             # Python version hint
├── .env.example            # Environment variable template
├── commands/
│   ├── tagall.py           # /all /tagall @all
│   ├── tagadmin.py         # /admin /tagadmin
│   ├── cancel.py           # /cancel
│   ├── sudo.py             # /addsudo /desudo /sudolist
│   ├── broadcast.py        # /broadcast /users
│   ├── funtag.py           # /gntag /gmtag /hitag /lifetag /shayari
│   ├── funtag_messages.py  # Fun tag message pools
│   └── forcejoin.py        # Force join gate
└── data/
    └── start_image.png     # Bot welcome image
```

---

## ⚠️ Important Notes

- The bot **must be made admin** in a group to read the full member list
- `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` come from [my.telegram.org](https://my.telegram.org) — they are **not** the bot token
- Force join checks require the bot to be a member of `@devilbots971` and `@devilbotsupport`
- Tagging large groups sends in batches of 5 with 1.5s delay to avoid Telegram flood limits

---

## 👨‍💻 Developer

Made with ❤️ by [@mrdevil12](https://t.me/mrdevil12)

- 📢 Channel: [@devilbots971](https://t.me/devilbots971)
- 💬 Support: [@devilbotsupport](https://t.me/devilbotsupport)
- 🐙 GitHub: [mrdevil42023](https://github.com/mrdevil42023)
