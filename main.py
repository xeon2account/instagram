from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start_handler import start
from handlers.download_handler import download_ig

app = Client("ig_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

app.add_handler(filters.command("start")(start))
app.add_handler(filters.text & ~filters.command(download_ig))

app.run()
