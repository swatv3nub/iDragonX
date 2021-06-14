import os
from config import PREFIX
from iDragonX import app, CMD_HELP
from iDragonX.helpers.run import run_cmd
from pyrogram import filters

CMD_HELP.update(
    {
        "Who": f"""
『 **• Who** 』
  `{PREFIX}who [name]` -> Search about a user all over the internet!
"""
    }
)

@app.on_message(filters.command("who", PREFIX))
async def who(_, message):
    msg = await message.reply_text(message, "`Searching For This User. This Can Take Upto 5 Minutes.`")
    user = message.text.split(None, 1)[1]
    if not user:
        await msg.edit("`Give Me Username As Input.`")
        return
    cmd = f"maigret {user} -n 150 -a --timeout 15  --pdf"
    await run_cmd(cmd)
    file = f"{user}.pdf"
    caption = f"OSINT For {user}."
    if not os.path.exists(file):
        await msg.edit("`Unable To Fetch Data. Maybe This User Likes To Keep A Air Of Mystery!`")
        return
    file_size = os.stat(file).st_size
    if file_size == 0:
        await msg.edit("`Unable To Fetch Data. Maybe This User Likes To Keep A Air Of Mystery!`")
        return
    if message.reply_to_message:
        await app.send_document(
            message.chat.id,
            file,
            caption=caption,
            reply_to_message_id=message.reply_to_message.message_id
        )
    else:
        await app.send_document(message.chat.id, file, caption=caption)
    if os.path.exists(file):
        os.remove(file)
    await msg.delete()