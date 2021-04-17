import os
from pyrogram import filters
from iDragonX import app
from config import PREFIX
import random
import time

p = 0


@app.on_message(filters.command("qbot", PREFIX) & filters.me)
async def quotly(_, m):
    if not message.reply_to_message:
        await message.edit_text("Reply to any users text message")
        return
    await message.edit_text("Making a Quote")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            msg = await app.get_history("@QuotLyBot", 1)
            check = msg[0]["sticker"]["file_id"]
            is_sticker = True
        except:
            time.sleep(0.5)
            progress += random.randint(0, 10)
            try:
                await message.edit_text(
                    f"```Making a Quote```\nProcessing {progress}%",
                    parse_mode="markdown",
                )
                if progress >= 100:
                    pass
            except Exception as ef:
                await message.edit_text(f"**ERROR:**\n{ef}", parse_mode="markdown")
                p += 1
                if p == 3:
                    break
    await message.edit_text("`Complete !`", parse_mode="markdown")
    msg_id = msg[0]["message_id"]
    await app.forward_messages(message.chat.id, "@QuotLyBot", msg_id)
    await app.read_history("@QuotLyBot")
    await message.delete()
