import asyncio
import time 
from pyrogram.types import Message, ChatPermissions
from pyrogram import filters
from pyrogram.errors import FloodWait, UserNotParticipant
from iDragonX import app, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "Commands": f"""
『 **• Stats** 』
  `{PREFIX}stats` -> fetchs stats.
"""
    }
)

async def mention_html(name: str, user_id: int) -> str:
    """Mention user in html format."""
    name = escape(name)
    return f'<a href="tg://user?id={user_id}">{name}</a>'

@app.on_message(filters.command(["stats", "stat"], PREFIX) & filters.me)
async def getstats(_, message: Message):
    await message.edit(
        "<b>Fetching stats...</b>"
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
<b><u>Stats:</u></b>
Total User:  <b>{gmen}</b>
<b>Private Chats:</b> <code>{private_chats}</code><code>
• Users: {gays_}
• Bots: {samx}</code>
<b>Groups:</b> <code>{fkg}</code>
<b>Channels:</b> <code>{fkc}</code>
<b>Admin in Groups:</b> <code>{fkg_a}</code><code>
• Creator: {fkg_o}
• Admin Rights: {fkg_a - fkg_o}</code>
<b>Admin in Channels:</b> <code>{fkc_a}</code><code>
• Creator: {fkc_o}
• Admin Rights: {fkc_a - fkc_o}</code>
<b>Unread Messages:</b> <code>{ffm}</code>
<b>Unread Mentions:</b> <code>{fmu}</code>
"""
    await message.edit(results)

