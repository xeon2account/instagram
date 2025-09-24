import os
import re
import threading
from flask import Flask
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from utils.ig_api import fetch_ig_media

# ✅ Flask app for Render health check or landing page
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Instagram Downloader Bot is running!"

# ✅ Pyrogram Telegram bot
bot = Client(
    "ig_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hi! I am your Instagram downloader bot.\n\n"
        "📥 Send me any Instagram **reel or post URL**, and I will download it!\n\n"
        "⚡ Example:\nhttps://www.instagram.com/reel/xyz123/"
    )

@bot.on_message(filters.text & ~filters.command("start"))
async def download_ig(client, message):
    raw_url = message.text.strip()
    clean_url = raw_url.split("?")[0].rstrip("/")

    INSTAGRAM_REGEX = re.compile(
        r"^https?://(www\.)?instagram\.com/(p|reel|tv)/[A-Za-z0-9_\-]+$"
    )

    if not INSTAGRAM_REGEX.match(clean_url):
        await message.reply_text("❌ Please send a valid Instagram post, reel, or IGTV URL.")
        return

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

# ✅ Start the bot in a background thread
# ✅ Start the bot in a background thread
def run_bot():
    bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    # Render provides the port in the $PORT env variable
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

