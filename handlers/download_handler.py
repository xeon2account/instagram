from pyrogram import filters
from utils.ig_api import fetch_ig_media

async def download_ig(client, message):
    url = message.text.strip()
    
    if "instagram.com" not in url:
        await message.reply_text("Please send a valid Instagram URL.")
        return
    
    data = fetch_ig_media(url)
    
    if data["status"] and data["data"]:
        media = data["data"][0]
        media_url = media["url"]
        media_type = media["type"]
        
        if media_type == "video":
            await message.reply_video(media_url, caption="Downloaded by xeon")
        else:
            await message.reply_text("Media type not supported yet.")
    else:
        await message.reply_text("Failed to download. Make sure the link is correct.")
