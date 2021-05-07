import os
import html
import tempfile
from pyrogram import filters
from iDragonX import app, progress_callback, session
from config import PREFIX

@app.on_message(filters.me & filters.command('open', PREFIX))
async def opentext(_, message):
    media = (message.text or message.caption).markdown.split(' ', 1)[1:]
    if media:
        media = os.path.expanduser(media[0])
    else:
        media = message.document
        if not media and not getattr(message.reply_to_message, 'empty', True):
            media = message.reply_to_message.document
        if not media:
            await message.reply_text('Document or local file path required')
            return
    done = False
    reply = rfile = None
    try:
        if not isinstance(media, str):
            rfile = tempfile.NamedTemporaryFile()
            reply = await message.reply_text('Downloading...')
            await app.download_media(media, file_name=rfile.name, progress=progress_callback, progress_args=(reply, 'Downloading...', False))
            media = rfile.name
        with open(media, 'rb') as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                if not chunk.strip():
                    continue
                chunk = f'<code>{html.escape(chunk.decode())}</code>'
                if done:
                    await message.reply_text(chunk, quote=False)
                else:
                    await getattr(reply, 'edit_text', message.reply_text)(chunk)
                    done = True
    finally:
        if rfile:
            rfile.close()
