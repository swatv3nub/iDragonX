import os

from telegraph import upload_file
from pyrogram import filters
from config import PREFIX
from iDragonX import app, CMD_HELP

CMD_HELP.update(
    {
        "Telegraph": f"""
『 **• Telegraph** 』
  `{PREFIX}tgphoto` - reply to a photo!
  `{PREFIX}tgvideo` - reply to a Video!
  `{PREFIX}tggif` - reply to a GIFs!
"""
    }
)

@app.on_message(filters.command("tgphoto", PREFIX) & filters.me)
async def tgphoto(_, message):
    if not message.reply_to_message.photo:
        await message.reply_text("Works only for Photos")
        return
    msg = await message.reply_text("`Uploading to Telegraph...`") 
    userid = str(message.chat.id)
    path = (f"./DOWNLOADS/{userid}.jpg")
    path = await app.download_media(message=message.reply_to_message, file_name=path)
    try:
      tlink = upload_file(path)
    except:
      await msg.edit_text("Something went Wrong.") 
    else:
      await msg.edit_text(f"Successfully Uploaded to [Telegraph](https://telegra.ph{tlink[0]})")     
      os.remove(path)
   
   
   
@app.on_message(filters.command("tgvideo", PREFIX) & filters.me)
async def tgvideo(_, message):
    if not message.reply_to_message.video:
        await message.reply_text("Works only for Videos")
        return
    if(message.video.file_size < 5242880):
        msg = await message.reply_text("Uploading to Telegraph...")
        userid = str(message.chat.id)
        vid_path = (f"./DOWNLOADS/{userid}.mp4")
        vid_path = await app.download_media(message=message.reply_to_message, file_name=vid_path)
        try:
          tlink = upload_file(vid_path)
          await msg.edit_text(f"Successfully Uploaded to [Telegraph](https://telegra.ph{tlink[0]})")   
          os.remove(vid_path)   
        except:
          await msg.edit_text("Something went Wrong.") 
    else:
        await message.reply_text("Size Should Be Less Than 5 mb")

      
@app.on_message(filters.command("tggif", PREFIX) & filters.me)
async def tggif(_, message):
    if not message.reply_to_message.animation:
        await message.reply_text("Works only for GIFs")
        return
    if(message.animation.file_size < 5242880):
        msg = await message.reply_text("Uploading to Telegraph...")
        userid = str(message.chat.id)
        gif_path = (f"./DOWNLOADS/{userid}.mp4")
        gif_path = await app.download_media(message=message.reply_to_message, file_name=gif_path)
        try:
          tlink = upload_file(gif_path)
          await msg.edit_text(f"Successfully Uploaded to [Telegraph](https://telegra.ph{tlink[0]})")   
          os.remove(gif_path)   
        except:
          await msg.edit_text("Something went Wrong.") 
    else:
        await message.reply_text("Size Should Be Less Than 5 mb")
