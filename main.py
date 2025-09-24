import os
import threading
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from utils.ig_api import fetch_ig_media
from flask import Flask

# ✅ Telegram Bot
app = Client(
    "./session/ig_downloader_bot",  # persistent session
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi! I am your Instagram downloader bot.\n"
        "Send me any Instagram reel or post URL, and I will download it!"
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_ig(client, message):
    url = message.text.strip()
    if "instagram.com" not in url:
        await message.reply_text("❌ Please send a valid Instagram URL.")
        return

    data = fetch_ig_media(url)
    if data.get("status") and data.get("data"):
        media = data["data"][0]
        media_url = media["url"]
        media_type = media["type"]
        if media_type == "video":
            await message.reply_video(media_url, caption="📥 Downloaded by Xeon Bot")
        else:
            await message.reply_text("❌ Media type not supported yet.")
    else:
        await message.reply_text("❌ Failed to download. Make sure the link is correct.")


# ✅ Dummy Flask server to satisfy Render's PORT scan
web = Flask(__name__)

@web.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))  # Render provides PORT
    web.run(host="0.0.0.0", port=port)

# ✅ Start Flask server in background & Pyrogram bot
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    app.run()
