import sys
import glob
import logging
import importlib
from pathlib import Path
from telethon import TelegramClient, events
from iDragonT import app, LOGGER
from iDragonT.modules import *

def load_plugins(plugin_name):
    path = Path(f"iDragonT/modules/{plugin_name}.py")
    name = "iDragonT.modules.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["iDragonT.modules." + plugin_name] = load

path = "iDragonT/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

app.start()
app.run_until_disconnected()
