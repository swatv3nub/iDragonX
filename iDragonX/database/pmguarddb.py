from iDragonX import mongo
import asyncio

collection = mongo["iDragonX"]["pmguard"]

PMGUARD_MESSAGE = (
    "`I'm a using an userbot in order to protect my PM from any kind of Spam.`"
    "`Please Wait for Me to come and Check Your Message\n\n`"
    "`Until then, Don't spam my PM, Or you'll get blocked and reported!`"
)

BLOCKED = "`Spammer Spotted! Successfully Blocked and Reported as Spam.`"

LIMIT = 5


async def set_pm(value: bool):
    doc = {"_id": 1, "pmguard": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await collection.find_one({"_id": 1})
    r2 = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": 1}, {"$set": {"pmguard": value}})
    else:
        await collection.insert_one(doc)
    if not r2:
        await collection.insert_one(doc2)


async def set_permit_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"pmguard_message": text}})


async def set_block_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await collection.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    pmguard = result["pmguard"]
    pm_message = result.get("pmguard_message", PMGUARD_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmguard, pm_message, limit, block_message


async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_approved_users():
    results = await collection.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await collection.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmguard"]:
        return False
    else:
        return True
