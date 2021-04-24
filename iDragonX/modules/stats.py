import asyncio
import time 
from pyrogram.types import ChatPermissions
from pyrogram import filters
from pyrogram.errors import FloodWait, UserNotParticipant
from iDragonX import app, CMD_HELP
from config import PREFIX


async def mention_html(name: str, user_id: int) -> str:
    """Mention user in html format."""
    name = escape(name)
    return f'<a href="tg://user?id={user_id}">{name}</a>'

async def admin_check(chat_id: int, user_id: int) -> bool:
    omk = await userge.get_chat_member(chat_id, user_id)
    done = ["creator", "administrator"]
    return omk.status in done

@app.on_message(filters.command(["stats", "stat"], PREFIX) & filters.me)
async def getstats(_, message):
    await message.edit_text(
        "**Fetching stats...**"
    )
    owner = await app.get_me()
    gmen = mention_html(owner.id, owner.first_name)
    fmu = 0
    ffm = 0
    private_chats = 0
    samx = 0
    gays_ = 0
    fkg = 0
    fkg_a = 0
    fkg_o = 0
    fkc = 0
    fkc_a = 0
    fkc_o = 0
    try:
        async for dialog in app.iter_dialogs():
            fmu += dialog.unread_mentions_count
            ffm += dialog.unread_messages_count
            chat_type = dialog.chat.type
            if chat_type in ["bot", "private"]:
                private_chats += 1
                if chat_type == "bot":
                    samx += 1
                else:
                    gays_ += 1
            else:
                try:
                    is_admin = await admin_check(dialog.chat.id, owner.id)
                    is_creator = dialog.chat.is_creator
                except UserNotParticipant:
                    is_admin = False
                    is_creator = False
                if chat_type in ["group", "supergroup"]:
                    groups += 1
                    if is_admin:
                        fkg_a += 1
                    if is_creator:
                        fkg_o += 1
                else:  # Channel
                    channels += 1
                    if is_admin:
                        fkc_a += 1
                    if is_creator:
                        fkc_o += 1
    except FloodWait as e:
        await asyncio.sleep(e.x + 5)

    results = f"""
**• Stats •**

**• Total User:** `{gmen}`
**• Private Chats:** `{private_chats}``
**• Groups:** `{fkg}`
**• Channels:** `{fkc}`
**• Admin in Groups:** `{fkg_a}``
**• Admin in Channels:** `{fkc_a}``
**• Unread Messages:** `{ffm}`
**• Unread Mentions:** `{fmu}`
"""
    await message.edit_text(results)
