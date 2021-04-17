import logging
import sys
import time
import pyromod.listen
from Python_ARQ import ARQ
from pyrogram import Client, errors
from config import API_HASH, API_ID, SESSION
import logging
#from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)

HELP = {}
CMD_HELP = {}

StartTime = time.time()

API_ID = API_ID
API_HASH = API_HASH
SESSION = SESSION

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

ARQ_API = "http://35.240.133.234:8000"
arq = ARQ(ARQ_API)

#cli = MongoClient(MONGO_DB_URI)