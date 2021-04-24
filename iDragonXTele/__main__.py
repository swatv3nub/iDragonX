import sys
import glob
import logging
import importlib
from pathlib import Path
from telethon import TelegramClient, events
from iDragonXTele import app, LOGGER
from iDragonXTele.plugs import *

def load_plugins(plugin_name):
    path = Path(f"iDragonXTele/plugs/{plugin_name}.py")
    name = "_telethon.modules.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["iDragonXTele.plugs." + plugin_name] = load

path = "iDragonXTele/plugs/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

app.start()
app.run_until_disconnected()
