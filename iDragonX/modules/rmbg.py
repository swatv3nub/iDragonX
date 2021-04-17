import os
from asyncio import sleep
import shutil
from removebg import RemoveBg
from iDragonX import app
from pyrogram import filters
from config import PREFIX, RMBG_API
from iDragonX.helpers.pyrohelpers import ReplyCheck


@app.on_message(filters.me & filters.command("rmbg", PREFIX))
async def remove_bg(_, m):
    if not RMBG_API:
        await m.edit_text(
            "Get the API from [REMOVE.BG](https://www.remove.bg/api)",
            disable_web_page_preview=True,
            parse_mode="html",
        )
        return
    replied = m.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        if os.path.exists("./downloads/img.jpg"):
            os.remove("./downloads/img.jpg")
        orig_pic = await c.download_media(
            message=replied, file_name="./downloads/img.jpg"
        )
        await m.edit_text("`Removing Background...`")
        try:
            rmbg = RemoveBg(RMBG_API, "rembg_error.log")
            rmbg.remove_background_from_img_file(orig_pic)
            remove_img = orig_pic + "_no_bg.png"
            new_rembg_file = orig_pic.replace(".jpg", "_rembg_app.png")
            shutil.move(remove_img, new_rembg_file)
            await c.send_document(
                chat_id=m.chat.id,
                document=new_rembg_file,
                caption="Background removed using iDragonX",
                reply_to_message_id=ReplyCheck(replied),
                disable_notification=True,
            )
            await m.delete()
            os.remove(new_rembg_file)
            os.remove(orig_pic)
        except Exception as ef:
            await m.edit_text(f"**Error:**\n\n`{ef}")
    return
