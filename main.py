import os
import re
import requests
from pyrogram import Client, filters

# ✅ Get Bot Token and API credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client(
    "insta_downloader",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# ✅ Flexible Instagram URL regex
INSTAGRAM_REGEX = re.compile(
    r"^https?://(www\.)?instagram\.com/(p|reel|tv)/[A-Za-z0-9_\-]+/?"
)

def fetch_ig_media(url: str):
    """Fetch media info from the API with timeout and error handling."""
    clean_url = url.split("?")[0]  # strip ?igsh=... etc
    api = f"https://api-aswin-sparky.koyeb.app/api/downloader/igdl?url={clean_url}"
    try:
        r = requests.get(api, timeout=15)
        r.raise_for_status()
        print("API raw response:", r.text)   # ✅ Debugging in Render logs
        return r.json()
    except requests.exceptions.RequestException as e:
        print("API request error:", e)
        return {"status": False, "error": str(e)}
    except ValueError:
        print("Invalid JSON from API")
        return {"status": False, "error": "Invalid JSON"}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hi! I am your Instagram downloader bot.\n\n"
        "Send me any Instagram post, reel, or IGTV URL and I will download it.\n\n"
        "Example:\nhttps://www.instagram.com/reel/xyz123/"
    )

@app.on_message(filters.text & ~filters.command("start"))
async def downloader(client, message):
    url = message.text.strip().split()[0]  # only first URL if multiple
    clean_url = url.split("?")[0]

    # ✅ Check if it is a valid Instagram link
    if not INSTAGRAM_REGEX.match(clean_url):
        await message.reply_text("❌ Please send a valid Instagram post, reel, or IGTV URL.")
        return

    data = fetch_ig_media(clean_url)

    if not data.get("status"):
        await message.reply_text("❌ Failed to download. API might be busy or the link is invalid.")
        return

    # ✅ Extract video or image link
    result = data.get("result", [])
    if not result:
        await message.reply_text("❌ No media found in the provided link.")
        return

    for item in result:
        if item.get("url"):
            await message.reply_video(
                item["url"],
                caption="📥 Downloaded by Xeon Bot"
            )

if __name__ == "__main__":
    app.run()
