import os
import re
import threading
import asyncio
import signal

from flask import Flask
from pyrogram import Client, filters, idle
from config import API_ID, API_HASH, BOT_TOKEN
from utils.ig_api import fetch_ig_media

bot = Client("ig_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Bot is alive!"

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi! I am your Instagram downloader bot.\n"
        "Send me any Instagram reel or post URL, and I will download it!"
    )

@bot.on_message(filters.text & ~filters.command("start"))
async def download_ig(client, message):
    url = message.text.strip()
    if "instagram.com" not in url:
        await message.reply_text("Please send a valid Instagram URL.")
        return

    data = fetch_ig_media(url)
    if data["status"] and data["data"]:
        media = data["data"][0]
        if media["type"] == "video":
            await message.reply_video(media["url"], caption="📥 Downloaded by Xeon Bot")
        else:
            await message.reply_text("❌ Media type not supported yet.")
    else:
        await message.reply_text("❌ Failed to download. Make sure the link is correct.")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start())
    loop.run_until_complete(idle())  # ✅ keeps bot alive

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
