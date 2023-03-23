import sqlite3

import discord
from discord.ext import commands
from discord import *
import datetime
import random
database = "db.db"
doubleWinRate = 50
Botid = int(1072269707614355507)
#Starting and Connecting to DB
con = sqlite3.connect(database)
cur = con.cursor()
try:
    cur.execute("CREATE TABLE coins(name TEXT, balance INTEGER)")
    cur.execute(f"INSERT INTO coins VALUES (1072269707614355507, 500000)")
    con.commit()
    print("Table Created")
except:
    print("Table Exists")
try:
    cur.execute("CREATE TABLE games(name INTEGER, bet INTEGER)")
    con.commit()
    print("Table Created")
except:
    print("Table Exists")

#Starting and Connecting to Discord
client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
TOKEN = open("tk.txt", "r")
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
#####################################################################################################################################

## Coinflip delete
@client.tree.command(name = "coinflipdelete")
@app_commands.describe(bet = "Coinflip Amount")
async def coinflip(interaction: discord.Interaction, bet: int):
    log = open("log.txt", "a")
    log.writelines(f"\nDouble Or Nothing Attempted By {interaction.user.mention} with a Value of {bet} {str(datetime.datetime.now())}")
    log.close()
    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    madeGame = [0,0]
    userid = interaction.user.id
    #Check if user is in database    
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        if int(userid) == int(row[0]):
            balance = row[1]
            print("old user")
            hit = [userid, balance]
    # Using Hit confirm is the user is in hit        
    if int(userid) == hit[0]:
        for row in cur.execute("SELECT name, bet FROM games ORDER by bet"):
            if userid == row[0]:
                if bet == row[1]:
                    madeGame = row
        if madeGame[0] == userid:
            if madeGame[1] == bet:
                cur.execute(f"DELETE FROM games WHERE name = {madeGame[0]} AND bet = {madeGame[1]}")
                con.commit()
                await interaction.response.send_message(f"Successfully deleted your Coinflip with a bet of {madeGame[1]}:coin:")
            else:
                await interaction.response.send_message(f"You do not have a Coinflip with this bet!")
        else:
            await interaction.response.send_message(f"You do not have a Coinflip game made. Use /Coinflip to make one!")        
    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
        con.commit()
        print(f"new user {userid}")
        await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")
    con.close()        


client.run(TOKEN)