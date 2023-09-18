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


@client.tree.command(name = "deposit")
@app_commands.describe(ticker = "Ticker", deposit = "Amount to deposit")
async def deposit(interaction: discord.Interaction, ticker: str, deposit: int):
    con = sqlite3.connect(database)
    cur = con.cursor()
    ticker = ticker.lower()
    if ticker == "c":
        userid = interaction.user.id
        hit = [0,0]
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            if int(userid) == int(row[0]): # Get user from Database
                balance = row[1]
                print("old user")
                hit = [userid, balance]        
        if int(userid) == hit[0]: # Continue if user is in Database
            balance = balance + deposit
            cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Set new balance
            con.commit()
            await interaction.response.send_message(f"Your balance is {balance}:coin:") # Success
            log = open("log.txt", "a")
            log.writelines(f"\n{interaction.user.id} Deposited {deposit} C {str(datetime.datetime.now())}")
            log.close()
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})") # Add User to Database
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Your balance is {deposit}:coin:")

    elif ticker == "db":
        userid = interaction.user.id
        hit = [0,0]
        deposit = deposit * 100
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            if int(userid) == int(row[0]): # Get user from Database
                balance = row[1]
                print("old user")
                hit = [userid, balance]        
        if int(userid) == hit[0]: # Continue if user is in Database           
                balance = balance + deposit
                cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Set new balance
                con.commit()
                await interaction.response.send_message(f"Your balance is {balance}:coin:") # Success
                log = open("log.txt", "a")
                log.writelines(f"\n{interaction.user.id} Deposited {deposit} DB {str(datetime.datetime.now())}")
                log.close()
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0 + int(deposit)})") # Add user to Database
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Your balance is {0 + int(deposit)}:coin:") # New user
    else:
        await interaction.response.send_message(f"Please Enter a Valid Ticker (T4)") # Error            
    con.close()
##############################################################################################################################################################

@client.tree.command(name = "withdraw")
@app_commands.describe(ticker = "Ticker", withdraw = "Amount to Withdaw")
async def withdraw(interaction: discord.Interaction, ticker: str, withdraw: int):
    con = sqlite3.connect(database)
    cur = con.cursor()
    ticker = ticker.lower()
    if ticker == "c":
        userid = interaction.user.id
        hit = [0,0]
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            if int(userid) == int(row[0]): # Get user from Database
                balance = row[1]
                print("old user")
                hit = [userid, balance]        
        if int(userid) == hit[0]: # Continue if user is in Database
            if balance >= withdraw:
                balance = balance - withdraw
                cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Set new balance
                con.commit()
                await interaction.response.send_message(f"Your balance is {balance}:coin:") # Success
                log = open("log.txt", "a")
                log.writelines(f"\n{interaction.user.id} Withdrew {withdraw} C {str(datetime.datetime.now())}")
                log.close()
            else:
                await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!") # Error
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})") # Add User to Database
            con.commit()
            await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!") # Error
    elif ticker == "db":
        userid = interaction.user.id
        hit = [0,0]
        withdraw = withdraw * 100
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            if int(userid) == int(row[0]): # Get user from Database
                balance = row[1]
                print("old user")
                hit = [userid, balance]        
        if int(userid) == hit[0]: # Continue if user is in Database
            if balance >= withdraw:
                balance = balance - withdraw
                cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Set new balance
                con.commit()
                await interaction.response.send_message(f"Your balance is {balance}:coin:") # Success
                log = open("log.txt", "a")
                log.writelines(f"\n{interaction.user.id} Withdrew {withdraw} DB {str(datetime.datetime.now())}")
                log.close()
            else:
                await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!")
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})") # Add User to Database
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!") # Error
    else:
        await interaction.response.send_message(f"Please Enter a Valid Ticker (T4)") # Error            
    con.close()        

#####################################################################################################################################
## User Balance
@client.tree.command()
async def cbalance(interaction: discord.Interaction):
    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    userid = interaction.user.id
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        if int(userid) == int(row[0]): # Get user from Database
            balance = row[1]
            print("old user")
            hit = [userid, balance]        
    if int(userid) == hit[0]: # Continue if user is in Database
        await interaction.response.send_message(f"Your balance is {balance}:coin:")
    else:
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})") # Add User to Database
        await interaction.response.send_message(f"Your balance is 0:coin:")
    con.close()

## Single Player Coinflip
@client.tree.command(name = "doubleornothing")
@app_commands.describe(bet = "Amount To Bet")
async def doubleornothing(interaction: discord.Interaction, bet: int):
    await games.doubleornothing(interaction, bet, doubleWinRate, playerTakings, botTakings, database, Botid)

## 2 Player Coinflip
@client.tree.command(name = "coinflip")
@app_commands.describe(bet = "Amount To Bet")
async def coinflip(interaction: discord.Interaction, bet: int):
    await games.coinflip(interaction, bet, playerTakings, botTakings, database, client)

## Coinflip delete
@client.tree.command(name = "coinflipdelete")
@app_commands.describe(bet = "Coinflip Amount")
async def coinflipDelete(interaction: discord.Interaction, bet: int):
    await games.coinflipdelete(interaction, bet, database)

## Coinflip list
@client.tree.command(name = "coinfliplist")
async def coinflipList(interaction: discord.Interaction):
    await games.coinflipList(interaction, database)
##############################################################################################################################################################
## DB and C Conversion
@client.tree.command(name = "convert")
@app_commands.describe(ticker = "Ticker", ticker2 = "Ticker 2", convert = "Amount to Convert")
async def convert(interaction: discord.Interaction, ticker: str, ticker2: str, convert: int):
    try:
        ticker = ticker.lower()
        ticker2 = ticker2.lower()
    except:
        await interaction.response.send_message(f"Please Enter Valid Tickers (T1)")
    print(ticker, ticker2, convert)
    if  ticker == "db" and ticker2 == "c":
        convert = convert * 100
# Get Bots Current Balance of C
# Check Bots Current Balance is Enough
# Get Customers Current Balance of DB
# Check Customers Balance is Enough
        print(convert)
        await interaction.response.send_message(f"/send c {interaction.user.mention} {convert}")

    elif ticker == "c" and ticker2 == "db":
# Get Bots current Balance of DB
# Check bots current balance is enough
# Get customers current balance of C
# Check customers Balance is enough
        convert = convert / 100

        if convert < 0.1 or convert == 0:
           await interaction.response.send_message(f"Please enter a value Divisible by 100")
        elif convert > 0:
            await interaction.response.send_message(f"/send db {interaction.user.mention} {convert}")
    else:
        await interaction.response.send_message(f"Please Enter Valid Tickers (T2)")
##############################################################################################################################################################
















#@client.tree.command(name= "auctioncreate")
#@app_commands.describe(command = "What would you like to do? (/auction help)", name = "What are you selling?", length = "How long will the auction last?", starting_bid = "Starting bid of the auction", buyout = "What amount would you ideally like to sell this item for?")
#async def auction(interaction: discord.Interaction, name: str, length: int, starting_bid: int, buyout: int):
#    try:
#        channel = "1082099666243551292"
#        print(f"Making an auction{str(name), str(length), str(starting_bid), str(buyout)}" )
#        await channel.create_thread(name = name, type=ChannelType.public_thread )
#        await interaction.response.send_message(f"I have created your auction")

#    except:
#        await interaction.response.send_message(f"Please ensure you have all the required information for your Auction. Use /auctionhelp for help")
#        print(name)



    



client.run(TOKEN)
