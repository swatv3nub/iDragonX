from pyrogram import idle, Client, filters
from iDragonX import app, teleapp, LOGGER
from config import PREFIX
from iDragonX.modules import *
        
print(f"iDragonX is now ready. Type {PREFIX}alive in any telegram chat.")

app.run()

