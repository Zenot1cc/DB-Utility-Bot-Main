import sqlite3

import discord
from discord.ext import commands
from discord import *
import datetime
import random
database = "db.db"
doubleWinRate = 50
playerTakings = 0.99
botTakings = 0.01
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
TOKEN = "MTA3MjI2OTcwNzYxNDM1NTUwNw.GGa4P0.OPDsKN3QyWiBv50OEU6Mttll0VbnUu1YJYyp9g"
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

## 2 Player Coinflip
@client.tree.command(name = "coinflip")
@app_commands.describe(bet = "Amount To Bet")
async def coinflip(interaction: discord.Interaction, bet: int):

    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    winnings = bet * 2
    userid = interaction.user.id    
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        if int(userid) == int(row[0]): # Get user from Database
            balance = row[1]
            print("old user")
            hit = [userid, balance]        
    if int(userid) == hit[0]: # Continue if user is in Database
        if balance >= bet:
            print("Valid Bet")
            newbalance = balance - bet
            cur.execute(f"UPDATE coins SET balance = {newbalance} WHERE name = {hit[0]}") # Remove Balance from Users account
            con.commit()
            gameMade = False
            oldnameid = 1
            for row in cur.execute("SELECT bet, name FROM games ORDER BY bet"):
                if bet == row[0]: # See if a game with this bet exists already
                    gameMade = True
                    oldnameid = row[1]
            if userid == oldnameid: # Make sure the user isnt betting against themselves
                await interaction.response.send_message(f"You cannot bet against yourself! Try /doubleornothing instead!")            
            else:
                if gameMade == True:
                    cur.execute(f"DELETE FROM games WHERE bet = {bet}") # Remove Game from Database if it is being played
                    con.commit()
                    pick = random.randint(1,2)
                    if pick == 1:
                        botTake = winnings * botTakings # Calculate bot and Players Takings
                        playerTake = winnings * playerTakings
                        round(botTake)
                        round(playerTake)
                        oldname = cur.execute(f"Select name, balance FROM coins WHERE name = {oldnameid}") # Get player 2s Id
                        balance = playerTake + int(oldname[1])
                        cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {oldname}") # Update Player 2s Balance
                        con.commit()
                        await interaction.response.send_message(f"@{oldname} Has won the Double or Nothing worth {winnings} :coin:") # Success
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {winnings} from {oldnameid} {str(datetime.datetime.now())}")
                        log.close()
                    else:
                        playerTake = winnings * playerTakings
                        botTake = winnings * botTakings
                        round(botTake)
                        round(playerTake)
                        balance = playerTake + hit[1] 
                        cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Update Player 1s Balance
                        con.commit()
                        await interaction.response.send_message(f"@{userid} Has won the Double or Nothing worth {bet} :coin:") # Success
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {bet} from {oldnameid} {str(datetime.datetime.now())}")
                        log.close()
                else:
                    cur.execute(f"INSERT INTO games VALUES ({userid}, {bet})") # Add Game to Database
                    con.commit()
                    await interaction.response.send_message(f"Created a Coinflip with a bet of {bet}:coin:. To cancel do /coinflipcancel {bet}") # Success
                    log = open("log.txt", "a")
                    log.writelines(f"\nCoinflip Created By {interaction.user.mention} with a Value of {bet} {str(datetime.datetime.now())}")
                    log.close()
        else:
            await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit") # Error
    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})") # Add User to Database
        con.commit()
        print(f"new user {userid}")
        await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit") # Error
    con.close()


client.run(TOKEN)