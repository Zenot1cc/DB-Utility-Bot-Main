import sqlite3

import discord
from discord.ext import commands
from discord import *
import datetime
import random
database = "db.db"
doubleWinRate = 45
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
TOKEN = "MTA3MjI2OTcwNzYxNDM1NTUwNw.GTJdvS.RbiDeoMGxvW_qwANUWHsFQKDI98E4BeymQM2Xc"
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

## 2 player coinflip
@client.tree.command(name = "coinflip")
@app_commands.describe(bet = "Amount To Bet")
async def coinflip(interaction: discord.Interaction, bet: int):
    log = open("log.txt", "a")
    log.writelines(f"\nDouble Or Nothing Attempted By {interaction.user.mention} with a Value of {bet} {str(datetime.datetime.now())}")
    log.close()
    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    winnings = bet * 2
    userid = interaction.user.id    
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        #Check if user is in database
        if int(userid) == int(row[0]):
            balance = row[1]
            print("old user")
            hit = [userid, balance]

    # Using Hit confirm is the user is in hit        
    if int(userid) == hit[0]:
        if balance >= bet:
            print("Valid Bet")
            newbalance = balance - bet
            #Remove bet from betters account
            cur.execute(f"UPDATE coins SET balance = {newbalance} WHERE name = {hit[0]}")
            con.commit()
            gameMade = False
            oldnameid = 1
            for row in cur.execute("SELECT bet, name FROM games ORDER BY bet"):
                if bet == row[0]:
                    gameMade = True
                    oldnameid = row[1]
            if userid == oldnameid:
                await interaction.response.send_message(f"You cannot bet against yourself! Try /doubleornothing instead!")
            
            else:
                if gameMade == True:
                    cur.execute(f"DELETE FROM games WHERE bet = {bet}")
                    con.commit()
                    pick = random.randint(1,2)
                    if pick == 1:
                        bet1 = winnings * 0.99
                        round(bet1)
                        oldname = cur.execute(f"Select name, balance FROM coins WHERE name = {oldnameid}")
                        print(oldname)
                        balance = bet1 + int(oldname[1])
                        cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {oldname}")
                        con.commit()
                        await interaction.response.send_message(f"@{oldname} Has won the Double or Nothing worth {winnings} :coin:")
                    else:
                        bet1 = winnings * 0.99
                        round(bet1)
                        balance = bet1 + hit[1]
                        cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
                        con.commit()
                        await interaction.response.send_message(f"@{userid} Has won the Double or Nothing worth {bet} :coin:")
                else:
                    cur.execute(f"INSERT INTO games VALUES ({userid}, {bet})")
                    con.commit()
                    await interaction.response.send_message(f"Created a Coinflip with a bet of {bet}:coin:. To cancel do /coinflipcancel {bet}")
        else:
            await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")
    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
        con.commit()
        print(f"new user {userid}")
        await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")
    con.close()        


client.run(TOKEN)