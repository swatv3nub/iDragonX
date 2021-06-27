from __future__ import unicode_literals
import asyncio
import os
import subprocess
import traceback
from sys import version as pyver
import youtube_dl
from pyrogram import filters
from pytgcalls import GroupCall

from iDragonX import app, arq, CMD_HELP
from config import PREFIX

from iDragonX.helpers.vchelpers import convert_seconds, download_and_transcode_song, time_to_seconds, transcode

CMD_HELP.update(
    {
        "VoiceChat": f"""
『 **• VoiceChat** 』
  `{PREFIX}play yt/deez song` -> Search and Play!
  `{PREFIX}pause` -> Pause the Song!
  `{PREFIX}vol [1~200]` -> Search and Play!
  `{PREFIX}skip` -> Skip the Song!
  `{PREFIX}resume` -> Resume the Song!
  `{PREFIX}tg` -> Pause from tg audio file!
"""
    }
)

SUDO = [1167145475, 1228116248, 1599519786]
queue = [] 
playing = False
call = {}


async def delete(message):
    await asyncio.sleep(10)
    await message.delete()

@app.on_message(
    filters.command("pause", PREFIX)
    & filters.user(SUDO)
)
async def pause_song(_, message):
    vc = call[str(message.chat.id)]
    vc.pause_playout()
    await message.reply_text(
        f"**Paused The Music, Send `{PREFIX}resume` To Resume.**", quote=False
    )


@app.on_message(
    filters.command("resume", PREFIX)
    & filters.user(SUDO)
)
async def resume_song(_, message):
    vc = call[str(message.chat.id)]
    vc.resume_playout()
    await message.reply_text(
        f"**Resumed, Send `{PREFIX}pause` To Pause The Music.**", quote=False
    )


@app.on_message(
    filters.command("vol", PREFIX)
    & filters.user(SUDO)
)
async def volume_bot(_, message):
    vc = call[str(message.chat.id)]
    usage = f"**Usage:**\n{PREFIX}vol [1~200]"
    if len(message.command) != 2:
        await message.reply_text(usage, quote=False)
        return
    volume = int(message.text.split(None, 1)[1])
    if (volume < 1) or (volume > 200):
        await message.reply_text(usage, quote=False)
        return
    try:
        await vc.set_my_volume(volume=volume)
    except ValueError:
        await message.reply_text(usage, quote=False)
        return
    await message.reply_text(f"**Volume Set To {volume}**", quote=False)


@app.on_message(
    filters.command("play", PREFIX)
    & filters.user(SUDO)
)
async def queuer(_, message):
    global queue
    try:
        usage = f"**Usage:**\n**{PREFIX}play yt/deez [song name]**"
        if len(message.command) < 3:
            await message.reply_text(usage, quote=False)
            return
        text = message.text.split(None, 2)[1:]
        service = text[0].lower()
        song_name = text[1]
        services = ["yt", "deez"]
        if service not in services:
            await message.reply_text(usage, quote=False)
            return
        await message.delete()
        if len(queue) > 0:
            await message.reply_text("**Added To Queue.**", quote=False)
        queue.append(
            {
                "service": service,
                "song": song_name,
                "message": message,
            }
        )
        await play()
    except Exception as e:
        e = traceback.format_exc()
        print(e)
        await message.reply_text(str(e), quote=False)


@app.on_message(filters.command("skip", PREFIX) & filters.user(SUDO))
async def skip(_, message):
    global playing
    if len(queue) == 0:
        await message.reply_text(
            "**Queue Is Empty.**", quote=False
        )
        return
    playing = False
    await message.reply_text("**Skipped!**", quote=False)
    await play()


@app.on_message(
    filters.command("queue", PREFIX)
    & filters.user(SUDO)
)
async def queue_list(_, message):
    if len(queue) != 0:
        i = 1
        text = ""
        for song in queue:
            text += (
                f"**{i}. Platform:** **{song['service']}** "
                + f"| **Song:** **{song['song']}**\n"
            )
            i += 1
        m = await message.reply_text(text, quote=False)
        await delete(message)
        await m.delete()

    else:
        m = await message.reply_text(
            "**Queue Is Empty, Just Like Your Life.**", quote=False
        )
        await delete(message)
        await m.delete()


# Queue handler


async def play():
    global queue, playing
    while not playing:
        await asyncio.sleep(0.1)
        if len(queue) != 0:
            service = queue[0]["service"]
            song = queue[0]["song"]
            message = queue[0]["message"]
            if service == "yt":
                playing = True
                del queue[0]
                try:
                    await ytplay(song, message)
                except Exception as e:
                    print(str(e))
                    playing = False
                    pass
            elif service == "deez":
                playing = True
                del queue[0]
                try:
                    await deezer(song, message)
                except Exception as e:
                    print(str(e))
                    playing = False
                    pass


# Deezer----------------------------------------------------------------------------------------


async def deezer(query, message):
    global playing
    m = await message.reply_text(
        f"**Searching for {query} on Deezer.**", quote=False
    )
    try:
        songs = await arq.deezer(query, 1)
        if not songs.ok:
            await message.reply_text(songs.result)
            return
        songs = songs.result
        title = songs[0].title
        duration = convert_seconds(int(songs[0].duration))
        thumbnail = songs[0].thumbnail
        artist = songs[0].artist
        url = songs[0].url
    except Exception:
        await m.edit("**Found No Song Matching Your Query.**")
        playing = False
        return
    await m.edit("**Downloading And Transcoding.**")
    await download_and_transcode_song(url)
    await m.delete()
    caption = (
        f"🏷 **Name:** [{title[:35]}]({url})\n⏳ **Duration:** {duration}\n"
        + "📡 **Platform:** Deezer"
    )
    m = await message.reply_text(caption)
    await asyncio.sleep(int(songs[0]["duration"]))
    await m.delete()
    playing = False

# Youtube Play-----------------------------------------------------


async def ytplay(query, message):
    global playing
    ydl_opts = {"format": "bestaudio"}
    m = await message.reply_text(
        f"**Searching for {query} on YouTube.**", quote=False
    )
    try:
        results = await arq.youtube(query)
        if not results.ok:
            await message.reply_text(results.result)
            return
        results = results.result
        link = f"https://youtube.com{results[0].url_suffix}"
        title = results[0].title
        thumbnail = results[0].thumbnails[0]
        duration = results[0].duration
        views = results[0].views
        if time_to_seconds(duration) >= 1800:
            await m.edit("**Only songs within 30 Mins.**")
            playing = False
            return
    except Exception as e:
        await m.edit("**Found No Song Matching Your Query.**")
        playing = False
        print(str(e))
        return
    await m.edit("**Downloading Music.**")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    await m.edit("**Transcoding.**")
    os.rename(audio_file, "audio.webm")
    transcode("audio.webm")
    await m.delete()
    caption = (
        f"🏷 **Name:** [{title[:35]}]({link})\n⏳ **Duration:** {duration}\n"
        + "📡 **Platform:** YouTube"
    )
    m = await message.reply_text(caption)
    await asyncio.sleep(int(time_to_seconds(duration)))
    playing = False
    await m.delete()


# Telegram Audio------------------------------------


@app.on_message(
    filters.command("tg", PREFIX) & filters.user(SUDO))
async def tgplay(_, message):
    global playing
    if len(queue) != 0:
        await message.reply_text(
            "**You Can Only Play Telegram Files After The Queue Gets "
            + "Finished.**",
            quote=False,
        )
        return
    if not message.reply_to_message:
        await message.reply_text("**Reply to an audio.**", quote=False)
        return
    if message.reply_to_message.audio:
        if int(message.reply_to_message.audio.file_size) >= 104857600:
            await message.reply_text(
                "**Only songs within 100 MB.**", quote=False
            )
            playing = False
            return
        duration = message.reply_to_message.audio.duration
        if not duration:
            await message.reply_text(
                "**Only Songs With Duration Are Supported.**", quote=False
            )
            return
        m = await message.reply_text("**Downloading.**", quote=False)
        song = await message.reply_to_message.download()
        await m.edit("**Transcoding.**")
        transcode(song)
        await m.edit(f"**Playing** **{message.reply_to_message.link}.**")
        await asyncio.sleep(duration)
        playing = False
        return
    await message.reply_text(
        "**Only Audio Files (Not Document) Are Supported.**", quote=False
    )
