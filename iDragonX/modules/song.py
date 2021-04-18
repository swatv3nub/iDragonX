from pyrogram import filters
import asyncio
import os
import aiohttp
import aiofiles
from random import randint
from pytube import YouTube
from youtubesearchpython import VideosSearch
from tswift import Song
from iDragonX.helpers.pyrohelper import get_arg
from iDragonX import app, arq, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "Music": f"""
『 **• Music** 』
  `{PREFIX}yt` -> Search For Songs in YouTube!
  `{PREFIX}deez` -> Search For Song in Deezer!
  `{PREFIX}lyrics` -> Search for Song Lyrics!
"""
    }
)

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url

async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return song_name

is_downloading = False

@app.on_message(filters.me & filters.command(["song", "yt"], PREFIX))
async def song(_, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter Song name properly.")
        return ""
    status = await message.reply("Searching!!")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("404: Song Unavailable, Make sure you typed correctly.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed: Download Unavailable")
        LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")

@app.on_message(filters.command("deez", PREFIX) & filters.me)
async def deezsong(_, message):
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text(f"{PREFIX}deez needs a argument")
        return
    if is_downloading:
        await message.reply_text("Serber Down Saar! Try 2 minutes later")
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("Searching...")
    try:
        songs = await arq.deezer(query, 1)
        title = songs[0].title
        url = songs[0].url
        artist = songs[0].artist
        await m.edit("Downloading")
        song = await download_song(url)
        await m.edit("Transcoding")
        await message.reply_audio(audio=song, title=title,
                                  performer=artist)
        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit(str(e))
        return
    is_downloading = False

@app.on_message(filters.command("lyrics", PREFIX) & filters.me)
async def get_lyrics(_, message):
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply(f"{PREFIX}lyrics need a Proper Argument")
        return ""
    m = await message.reply_text(f"**Finding lyrics for:** `{args}`")
    song = Song.find_song(args)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Couldn't find any lyrics for that song!"
    else:
        reply = "Song not found!"
    if len(reply) > 4090:
        with open("lyrics.txt", "w") as f:
            f.write(reply)
            f.close()
        await m.reply_document(
            document="lyrics.txt",
            caption=("Message length exceeded max limit! " "Sent as a text file."),
        )
        os.remove("lyrics.txt")
        await m.delete()
    else:
        await m.edit_text(reply)
    return
