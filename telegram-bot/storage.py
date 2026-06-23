import os
from supabase import create_client, Client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def db() -> Client:
    return _client

def get_users():
    try:
        res = db().table("bot_users").select("user_id, name, username").order("name").execute()
        return res.data or []
    except Exception:
        return []

def add_user(user_id: int, name: str, username: str = None):
    try:
        db().table("bot_users").upsert({
            "user_id": user_id,
            "name": name or str(user_id),
            "username": username,
        }, on_conflict="user_id").execute()
    except Exception:
        pass

def get_groups():
    try:
        res = db().table("bot_groups").select("chat_id, title, username").order("title").execute()
        return res.data or []
    except Exception:
        return []

def add_group(chat_id: int, title: str, username: str = None):
    try:
        db().table("bot_groups").upsert({
            "chat_id": chat_id,
            "title": title or str(chat_id),
            "username": username,
        }, on_conflict="chat_id").execute()
    except Exception:
        pass

def get_sudo_users(chat_id: int):
    try:
        res = (
            db().table("sudo_users")
            .select("user_id")
            .eq("chat_id", chat_id)
            .execute()
        )
        return [str(row["user_id"]) for row in (res.data or [])]
    except Exception:
        return []

def add_sudo_user(chat_id: int, user_id: int):
    try:
        db().table("sudo_users").upsert({
            "chat_id": chat_id,
            "user_id": user_id,
        }, on_conflict="chat_id,user_id").execute()
    except Exception:
        pass

def remove_sudo_user(chat_id: int, user_id: int):
    try:
        db().table("sudo_users").delete().eq("chat_id", chat_id).eq("user_id", user_id).execute()
    except Exception:
        pass
