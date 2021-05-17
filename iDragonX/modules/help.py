from pyrogram import filters
from iDragonX import app, HELP, CMD_HELP
from config import PREFIX
from iDragonX.helpers.pyrohelper import get_arg

HELP.update(
    {
        "**Admin**": "ban, unban, promote, demote, kick, mute, unmute, pin, purge, del, invite, delghosts",
        "**Alive**": "alive, ping",
        "**Info**": "whois, id",
        "**Exec**": "exec, cexac, eval, evalx, sh",
        "**Misc**": "paste, tr, qbot, rmbg, zip, unzip, open, encode, decode",
        "**Sticker**": "kang, stickerinfo",
        "**Music**": "yt, deez, lyrics",
        "**Search**": "go, sof, git, reddit, define",
        "**SpamCheck**": "spamcheck, anon, deai, spb, sw, cas, rose",
        "**Voice Chat**": "play, pause, resume, vol, queue"
    }
)


@app.on_message(filters.command("help", PREFIX) & filters.me)
async def help(client, message):
    args = get_arg(message)
    if not args:
        text = "**Available Commands**\n\n"
        for key, value in HELP.items():
            text += f"{key}: {value}\n\n"
        await message.edit(text)
        return
    else:
        module_name = args
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            await message.edit("Invalid module name specified.")
            return
        else:
            await message.edit(module_help)
