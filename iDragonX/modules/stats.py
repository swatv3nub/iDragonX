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

@app.on_message(filters.command(["stats", "stat"], PREFIX) & filters.me)
async def getstats(_, message):
    x = await message.reply_text(
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
            unread_mentions += dialog.unread_mentions_count
            unread_msg += dialog.unread_messages_count
            chat_type = dialog.chat.type
            if chat_type in ["bot", "private"]:
                private_chats += 1
                if chat_type == "bot":
                    bots += 1
                else:
                    users_ += 1
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
                        groups_admin += 1
                    if is_creator:
                        groups_creator += 1
                else:  # Channel
                    channels += 1
                    if is_admin:
                        channels_admin += 1
                    if is_creator:
                        channels_creator += 1
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
    await x.exit_text(results)
