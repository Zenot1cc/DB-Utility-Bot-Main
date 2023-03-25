import discord
from discord.ext import commands
from discord import *
import random
import datetime
import sqlite3
database = "db.db"
Botid = int(1072269707614355507)
doubleWinRate = 50
playerTakings = 0.99
botTakings = 0.01
TOKEN = "MTA3MjI2OTcwNzYxNDM1NTUwNw.GTJdvS.RbiDeoMGxvW_qwANUWHsFQKDI98E4BeymQM2Xc"

#Starting and Connecting to DB
con = sqlite3.connect(database)
cur = con.cursor()
try:
    cur.execute("CREATE TABLE coins(name INTEGER, balance INTEGER)")
    cur.execute("CREATE TABLE games(gameName STRING, name INTEGER, bet INTEGER)")

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
##############################################################################################################################################################
## Single Player Coinflip
@client.tree.command(name = "doubleornothing")
@app_commands.describe(bet = "Amount To Bet")
async def coinflip(interaction: discord.Interaction, bet: int):
    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    winnings = bet * 2
    BotTake = winnings * botTakings
    playerTake = winnings * playerTakings
    userid = interaction.user.id    
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        if int(userid) == int(row[0]): # Get user from Database
            balance = row[1]
            print("old user")
            hit = [userid, balance]
        if int(Botid) == int(row[0]): # Get bot from Database
            botBal = int(row[1])
            print(botBal)
    if userid == hit[0]: # Continue is user is in Database
        if balance >= bet:
            if botBal > winnings:
                newbal = balance - bet
                cur.execute(f"UPDATE coins SET balance = {newbal} WHERE name = {userid}") # Remove Balance from Users Account
                con.commit()
                dice = random.randint(0,100)
                if dice < doubleWinRate:
                    balance = balance + playerTake
                    botBal = botBal - playerTake
                    cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Add winnings to Users Account
                    cur.execute(f"UPDATE coins SET balance = {botBal} WHERE name = {Botid}") # Remove Winnings from Bots Account
                    con.commit()
                    await interaction.response.send_message(f"You won! Your balance is {balance}:coin:") # Success
                    log = open("log.txt", "a")
                    log.writelines(f"\nDouble Or Nothing Won By {interaction.user.mention} with a Value of {winnings} {str(datetime.datetime.now())}")
                    log.close()
                    log = open("botGambleWinnings.txt", "a")
                    log.writelines(f"\nBot took {BotTake}")
                    log.close()
                else:
                    botBal = botBal + int(playerTake)
                    cur.execute(f"UPDATE coins SET balance = {botBal} WHERE name = {Botid}") # Add winnings to Bots Account
                    con.commit()
                    await interaction.response.send_message(f"The house has won. Better luck next time!") # Success
                    log = open("log.txt", "a")
                    log.writelines(f"\nDouble Or Nothing Won By Bot with a Value of {winnings} {str(datetime.datetime.now())}")
                    log.close()
                    log = open("botGambleWinnings.txt", "a")
                    log.writelines(f"\nBot took {BotTake}")
                    log.close()
            else:
                await interaction.response.send_message(f"Bot does not have enough :coin: for this action!") # Error
        else:
            await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit") # Error
    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})") # Add User to Database
        con.commit()
        await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit") # Error
    con.close()
##############################################################################################################################################################
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
            olduserid = 1
            for row in cur.execute("SELECT bet, name FROM games ORDER BY bet"):
                if bet == row[0]: # See if a game with this bet exists already
                    gameMade = True
                    olduserid = row[1]
            if userid == olduserid: # Make sure the user isnt betting against themselves
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
                        oldname = cur.execute(f"Select name, balance FROM coins WHERE name = {olduserid}") # Get player 2s Balance
                        balance = playerTake + int(olduserid[1])
                        cur.execute(f"UPDATE coins SET balance = {int(balance)}) WHERE name = {oldname}") # Update Player 2s Balance
                        con.commit()
                        await interaction.response.send_message(f"@{oldname} Has won the Double or Nothing worth {winnings} :coin:") # Success
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {winnings} from {oldnameid} {str(datetime.datetime.now())}")
                        log.close()
                        log = open("botGambleWinnings.txt", "a")
                        log.writelines(f"\nBot took {int(botTake)}")
                        log.close()
                    else:
                        playerTake = winnings * playerTakings
                        botTake = winnings * botTakings
                        round(botTake)
                        round(playerTake)
                        balance = playerTake + newbalance 
                        cur.execute(f"UPDATE coins SET balance = {int(balance)} WHERE name = {userid}") # Update Player 1s Balance
                        con.commit()
                        await interaction.response.send_message(f"@{userid} Has won the Double or Nothing worth {bet} :coin:") # Success
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {bet} from {olduserid} {str(datetime.datetime.now())}")
                        log.close()
                        log = open("botGambleWinnings.txt", "a")
                        log.writelines(f"\nBot took {int(botTake)}")
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
#####################################################################################################################################

## Coinflip delete
@client.tree.command(name = "coinflipdelete")
@app_commands.describe(bet = "Coinflip Amount")
async def coinflipDelete(interaction: discord.Interaction, bet: int):
    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    madeGame = [0,0]
    userid = interaction.user.id
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        if int(userid) == int(row[0]): # Get user from Database
            balance = row[1]
            print("old user")
            hit = [userid, balance]        
    if int(userid) == hit[0]: # Continue if user is in Database
        for row in cur.execute("SELECT name, bet FROM games ORDER by bet"):
            if userid == row[0]:
                if bet == row[1]:
                    madeGame = row
        if madeGame[0] == userid:
            if madeGame[1] == bet:
                balance = int(balance) + bet
                cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}") # Update Players Balance
                cur.execute(f"DELETE FROM games WHERE name = {madeGame[0]} AND bet = {madeGame[1]}") # Delete Game
                con.commit()
                await interaction.response.send_message(f"Successfully deleted your Coinflip with a bet of {madeGame[1]}:coin:") # Success
                log = open("log.txt", "a")
                log.writelines(f"\nCoinflip Deleted by {interaction.user.mention} with a Value of {bet} {str(datetime.datetime.now())}")
                log.close()
            else:
                await interaction.response.send_message(f"You do not have a Coinflip with this bet!") # Error
        else:
            await interaction.response.send_message(f"You do not have a Coinflip game made. Use /Coinflip to make one!") # Error        
    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
        con.commit()
        print(f"new user {userid}")
        await interaction.response.send_message(f"You do not have a Coinflip game made. Use /Coinflip to make one!") # Error 
    con.close()
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
