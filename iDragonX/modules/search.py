from iDragonX import app, arq
from pyrogram import filters
from config import PREFIX
from search_engine_parser import GoogleSearch
from pyrogram.types import Message
from requests import get

@app.on_message(filters.command("go", PREFI ))
@capture_err
async def google(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/go Needs An Argument")
            return
        text = message.text.split(None, 1)[1]
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))


# StackOverflow [This is also a google search with some added args]


@app.on_message(filters.command("sof", PREFIX))
@capture_err
async def stack(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text('/sof Needs An Argument')
            return
        gett = message.text.split(None, 1)[1]
        text = gett + ' "site:stackoverflow.com"'
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))


# Github [This is also a google search with some added args]


@app.on_message(filters.command("git", PERFIX))
@capture_err
async def github(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text('/git Needs An Argument')
            return
        gett = message.text.split(None, 1)[1]
        text = gett + ' "site:github.com"'
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))

@app.on_message(filters.command("reddit", PREFIX))
@capture_err
async def reddit(_, message):
    if len(message.command) != 2:
        await message.reply_text("/reddit needs an argument")
        return
    subreddit = message.text.split(None, 1)[1]
    try:
        reddit = await arq.reddit(subreddit)
        sreddit = reddit.subreddit
        title = reddit.title
        image = reddit.url
        link = reddit.postLink
        caption = f"""**Title:** `{title}`
**Subreddit:** {sreddit}
**PostLink:** {link}"""
        await message.reply_photo(photo=image, caption=caption)
    except Exception as e:
        print(str(e))
        await message.reply_text(str(e))

@app.on_message(filters.command("define", PREFIX))
@capture_err
async def urbandict(_, message):
    if len(message.command) < 2:
        await message.reply_text("/define Needs An Argument.")
        return
    text = message.text.split(None, 1)[1]
    api = "http://api.urbandictionary.com/v0/define?term="

    try:
        results = get(f"{api}{text}").json()
        reply_text = f'**Definition:** {results["list"][0]["definition"]}'
        reply_text += f'\n\n**Example:** {results["list"][0]["example"]}'
    except IndexError:
        reply_text = ("**404:** Nothing Found!")
    ignore_chars = "[]"
    reply = reply_text
    for chars in ignore_chars:
        reply = reply.replace(chars, "")
    if len(reply) >= 4096:
        reply = reply[:4096]
    await message.reply_photo(photo="https://telegra.ph/file/0a166031f43ef8271e813.jpg", caption=reply)
