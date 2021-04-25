import sys
import glob
import logging
import importlib
from pathlib import Path
from pyrogram import idle, Client, filters
from telethon import TelegramClient, events
from iDragonX import app, teleapp, LOGGER
from config import PREFIX
from iDragonX.modules import *

def load_plugins(plugin_name):
    path = Path(f"iDragonX/modules/{plugin_name}.py")
    name = "iDragonX.modules.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["iDragonX.modules." + plugin_name] = load

path = "iDragonX/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
        
print(f"iDragonX is now ready. Type {PREFIX}alive in any telegram chat.")

app.run()
teleapp.start()
teleapp.run_until_disconnected()

