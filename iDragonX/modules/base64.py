"""Encoding and Decoding Base64"""

import pybase64
from pyrogram import filters
from iDragonX import app, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "Base64": f"""
『 **• Base64** 』
  `{PREFIX}encode` -> Encode in Base64!
  `{PREFIX}decode` -> Decode from Base64!
"""
    }
)

@app.on_message(
    filters.command("encode", PREFIX))
async def encode(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a Message!")
        return
    else:
        inputz = message.reply_to_message.text
        out = str(pybase64.b64encode(bytes(inputz, "utf-8")))[2:-1]
        await message.reply_text(f"**Encoded in Base64** : `{out}`", parse_mode="markdown")
        
@app.on_message(filters.command("decode", PREFIX))
async def decode(_, messags):
    if not message.reply_to_message:
        await message.reply_text("Reply to a Message!")
        return
    else:
        inputx = message.reply_to_message.text
        out = str(pybase64.b64decode(bytes(inputx, "utf-8"), validate=True))[2:-1]
        await message.reply_text(f"**Decoded from Base64** : `{out}`", parse_mode="markdown")