from iDragonX import app
from pyrogram import filters
from pyrogram.types import Message
from config import PREFIX
import os
from asyncio import sleep


@app.on_message(filters.command("delghosts", PREFIX) & filters.me)
async def delghost(_, m):
    if len(m.text.split()) == 1:
        await m.edit_text("`Counting deleted accounts!!!`")
        del_users = []
        u = 0
        async for x in app.iter_chat_members(chat_id=m.chat.id):
            if x.user.is_deleted:
                del_users.append(x.user.id)
        if del_users:
            await m.edit_text(
                f"`Found {len(del_users)} Ghost!` Cleaning Them in less than {len(del_users)}s"
            )
        else:
            await m.edit_text("No Ghost Accounts Found!")
        async for x in app.iter_chat_members(chat_id=m.chat.id):
            await sleep(0.1)
            if x.user.is_deleted:
                del_users.append(x.user.id)
                a = await app.get_chat_member(m.chat.id, x.user.id)
                if a.user.status not in ("administrator", "creator"):
                    try:
                        await app.kick_chat_member(m.chat.id, x.user.id)
                        u += 1
                        await sleep(0.1)
                    except:
                        pass
        await m.edit_text(f"**Group Cleaned!**\nRemoved `{u}` Ghosts")
    else:
        await m.edit_text(
            f"Check {PREFIX}help properly!"
        )
    return
