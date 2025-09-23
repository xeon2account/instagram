from pyrogram import filters

async def start(client, message):
    await message.reply_text("Hi! Send me an Instagram reel or video URL and I'll download it.")
