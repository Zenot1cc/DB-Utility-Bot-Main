import discord
from discord.ext import commands
from discord import *
import datetime
import sqlite3
import games
database = "db.db"
Botid = int(1072269707614355507)
doubleWinRate = 50
playerTakings = 0.99
botTakings = 0.01
TOKEN = open("tk", "r")
TOKEN = TOKEN.read()
#Starting and Connecting to DB
con = sqlite3.connect(database)
cur = con.cursor()
try:
    cur.execute("CREATE TABLE coins(name INTEGER, balance INTEGER)")
    print("Table Created")
    cur.execute(f"INSERT INTO coins VALUES ({Botid}, 0)")
    con.commit()
except:
    print("Table Exists")

try:
    cur.execute("CREATE TABLE games(name INTEGER, bet INTEGER)")
    print("Table Created")
    cur.execute(f"INSERT INTO coins VALUES ({Botid}, 0)")
    con.commit()
except:
    print("Table Exists")
con.close()

#Starting and Connecting to Discord
intents = discord.Intents().all()
client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@client.event
async def on_ready():
    print("ready")
    try:
        synced = await client.tree.sync()
        print(f"Synced", len(synced))
        log = open("log.txt", "a")
        log.writelines(f"\nBot Started and Synced Successfully{str(datetime.datetime.now())}")
        log.close()
    except Exception as e:
        print(e)
        log = open("log.txt", "a")
        log.writelines(f"\nBot Started but Unable to sync ({e}) {str(datetime.datetime.now())}")
        log.close()

        