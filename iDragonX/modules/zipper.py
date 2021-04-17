import shutil
import os
from iDragonX import app, CMD_HELP
from pyrogram import filters
from config import PREFIX

CMD_HELP.update(
    {
        "Zipper": f"""
『 **• Zipper** 』
  `{PREFIX}zip <folder> -> to zip the folder
  `{PREFIX}unzip <file>`-> to unzip the file
"""
    }
)


async def zipdir(path):
    if path.endswith("/"):
        path = path[0:-1]
    filename = path.split("/")[-1]
    shutil.make_archive(filename, "zip", path)
    return filename + ".zip"


async def unzipfiles(zippath):
    foldername = zippath.split("/")[-1]
    extract_path = f"/root/iDragonX/cache/unzip/{foldername}"
    shutil.unpack_archive(zippath, extract_path)
    return extract_path


@app.on_message(filters.command("zip", PREFIX) & filters.me)
async def zipit(_, m):

    if (m.command) == 1:
        await m.edit_text("Please enter a directory path to zip!")
        return

    location = m.text.split(None, 1)[1]
    await m.edit_text("Zipping file...")
    filename = await zipdir(location)
    await m.edit_text(
        f"File zipped and saved to `/root/{filename}`, to upload, use `{PREFIX}upload {filename}`"
    )
    return


@app.on_message(filters.command("unzip", PREFIX) & filters.me)
async def unzipit(_, m):

    if (m.command) == 1:
        await m.edit_text("Please enter path to zip file which you want to extract!")
        return

    fileLoc = m.text.split(None, 1)[1]
    await m.edit_text("Unzipping file...")
    extract_path = await unzipfiles(fileLoc)
    await m.edit_text(f"Files unzipped to `{extract_path}`.")
    return
