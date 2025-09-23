from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from utils.ig_api import fetch_ig_media
import re

app = Client("ig_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi! I am your Instagram downloader bot.\n"
        "Send me any Instagram reel or post URL, and I will download it!"
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_ig(client, message):
    url = message.text.strip()

    # ✅ Clean Instagram URL
    clean_url = url.split("?")[0].rstrip("/")

    # ✅ Regex check
    if not re.match(r"^https?://(www\.)?instagram\.com/(p|reel|tv)/[A-Za-z0-9_\-]+$", clean_url):
        await message.reply_text("❌ Please send a valid Instagram post, reel, or IGTV URL.")
        return

    data = fetch_ig_media(clean_url)
    if data["status"] and data["data"]:
        media = data["data"][0]
        media_url = media["url"]
        media_type = media["type"]
        if media_type == "video":
            await message.reply_video(media_url, caption="📥 Downloaded by Xeon")
        else:
            await message.reply_text("❌ Media type not supported yet.")
    else:
        await message.reply_text("❌ Failed to download. Make sure the link is correct.")

app.run()
