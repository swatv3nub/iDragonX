from iDragonX import app, CMD_HELP
from config import PREFIX, LOG_GROUP_ID
from pyrogram import filters
from iDragonX.database.globalcmdsdb import *
from iDragonX.helpers.pyrohelper import get_arg
from iDragonX.helpers.adminhelpers import CheckAdmin

CMD_HELP.update(
    {
        "Global": f"""
『 **• Global** 』
  `{PREFIX}gban` -> Globally ban an User!
  `{PREFIX}gmute` -> Globally Mute an User!
  `{PREFIX}ungban` -> Globally unban an user!
  `{PREFIX}ungmute` -> Globally unmute an user!
"""
    }
)

async def iter_chats(client):
    chats = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in ["supergroup", "channel"]:
            chats.append(dialog.chat.id)
    return chats


#gmute

@app.on_message(filters.command("gmute", PREFIX) & filters.me)
async def gmute(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Gmute Who?**")
            return
    get_user = await app.get_users(user)
    await gmute_user(get_user.id)
    await message.edit(f"**Gmuted {get_user.mention}!**")
    await app.send_message(LOG_GROUP_ID, f"Gmuted {get_user.mention}")

@app.on_message(filters.command("ungmute", PREFIX) & filters.me)
async def gmute(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Ungmute Who?**")
            return
    get_user = await app.get_users(user)
    await ungmute_user(get_user.id)
    await message.edit(f"**Ungmuted {get_user.first_name}!**")
    await app.send_message(LOG_GROUP_ID, f"Ungmuted {get_user.mention}")
    


@app.on_message(filters.group & filters.incoming)
async def check_and_del(client, message):
    if not message:
        return
    try:
        if not message.from_user.id in (await get_gmuted_users()):
            return
    except AttributeError:
        return
    message_id = message.message_id
    try:
        await app.delete_messages(message.chat.id, message_id)
    except:
        pass

#gban

@app.on_message(filters.command("gban", PREFIX) & filters.me)
async def gban(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**GBan Who?**")
            return
    get_user = await app.get_users(user)
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        message.edit("No Chats Found!")
        return
    await message.edit(f"Starting Global Bans of {get_user.first_name}!")
    for owo in chat_dict:
        try:
            await app.kick_chat_member(owo, int(get_user.id))
        except:
            pass
    await gban_user(get_user.id)
    await message.edit(f"**Gbanned {get_user.mention} in {chat_len} chats!**")
    await app.send_message(LOG_GROUP_ID, f"Gbanned {get_user.mention}")


@app.on_message(filters.command("ungban", PREFIX) & filters.me)
async def ungban(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Ungban Who?**")
            return
    get_user = await app.get_users(user)
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        message.edit("No Chats Found!")
        return
    await message.edit(f"Removing Global Bans of {get_user.first_name}!")
    for owo in chat_dict:
        try:
            await app.unban_chat_member(owo, int(get_user.id))
        except:
            pass
    await gban_user(get_user.id)
    await message.edit(f"**Ungbanned {get_user.mention} in {chat_len} chats!**")
    await app.send_message(LOG_GROUP_ID, f"Ungbanned {get_user.mention}")

    
@app.on_message(filters.group & filters.incoming)
async def check_and_ban(_, message):
    if not message:
        return
    if not message.from_user:
        return
    try:
        if not message.from_user.id in (await get_gbanned_users()):
            return
    except:
        return
    user = message.from_user["id"]
    try:
        admeme = await message.chat.get_member(int(app.me.id))
    except:
        return
    if not admeme.can_restrict_members:
        await message.reply("@admins\nThis User is Currently gbanned in my Userbot because of Active Spamming! Mind Muting or Banning this User.")
        return
    try:
        await app.kick_chat_member(message.chat.id, int(user))
        await client.send_message(message.chat.id, f"Gbanned User Spotted: [{user}](tg://user?id={user})\nSuccessfully Banned!")
    except:
        return