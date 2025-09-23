import os
import re
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from utils.ig_api import fetch_ig_media

# ✅ Create a folder to store the session file (persistent disk in Render)
SESSION_DIR = "./session"
os.makedirs(SESSION_DIR, exist_ok=True)

# ✅ Use persistent session path
app = Client(
    session_name=os.path.join(SESSION_DIR, "ig_downloader_bot"),
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi! I am your Instagram downloader bot.\n"
        "Send me any Instagram reel or post URL, and I will download it!\n\n"
        "⚡ Example: https://www.instagram.com/reel/xyz123/"
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_ig(client, message):
    raw_url = message.text.strip()

    # ✅ Clean URL (remove query params and trailing slash)
    clean_url = raw_url.split("?")[0].rstrip("/")

    # ✅ Regex to validate Instagram link
    INSTAGRAM_REGEX = re.compile(
        r"^https?://(www\.)?instagram\.com/(p|reel|tv)/[A-Za-z0-9_\-]+$"
    )

    if not INSTAGRAM_REGEX.match(clean_url):
        await message.reply_text("❌ Please send a valid Instagram post, reel, or IGTV URL.")
        return

    # ✅ Fetch media using API
    data = fetch_ig_media(clean_url)
    if not data.get("status") or not data.get("data"):
        await message.reply_text("❌ Failed to download. API might be busy or the link is invalid.")
        return

    media = data["data"][0]
    media_url = media["url"]
    media_type = media["type"]

    if media_type == "video":
        await message.reply_video(media_url, caption="📥 Downloaded by Xeon Bot")
    else:
        await message.reply_text("❌ Media type not supported yet.")

app.run()
