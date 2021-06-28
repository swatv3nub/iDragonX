from io import BytesIO
from pyrogram import filters
from iDragonX import app, session, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "Carbon": f"""
『 **• Carbon** 』
  `{PREFIX}carbon` -> Reply to a message to get it carbonised!
"""
    }
)

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with session.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "iDragonX.png"
    return image

@app.on_message(filters.command("carbon", PREFIX))
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a text message to make carbon."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Reply to a text message to make carbon."
        )
    msg = await message.reply_text("Being Carbonised...")
    carbon = await make_carbon(message.reply_to_message.text)
    await app.send_document(message.chat.id, carbon)
    await msg.delete()
    carbon.close()
