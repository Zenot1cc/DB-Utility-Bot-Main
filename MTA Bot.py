import discord
from discord.ext import commands
from discord import *
import random
import datetime
import sqlite3
database = "db.db"
Botid = int(1072269707614355507)
doubleWinRate = 50
TOKEN = open("tk.txt", "r")

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

    try:
        ticker.lower()
    except:
        await interaction.response.send_message(f"Please Enter a Valid Ticker (T3) ")

    if ticker == "c":
        userid = interaction.user.id
        hit = [0,0]
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            #Check if user is in database
            if int(userid) == int(row[0]):
                balance = row[1]
                print("old user")
                balance = int(row[1]) + int(deposit)
                print(balance)
                hit = [int(interaction.user.id), int(balance)]
            #If they are, Update Records
        if userid == hit[0]:
            cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
            con.commit()
            await interaction.response.send_message(f"Your balance is {balance}:coin:")
            log = open("log.txt", "a")
            log.writelines(f"\n{interaction.user.id} Deposited {deposit} C {str(datetime.datetime.now())}")
            log.close()
        #If not, Create Records
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0 + int(deposit)})")
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Your balance is {deposit}:coin:")

    elif ticker == "db":
        userid = interaction.user.id
        hit = [0,0]
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            #Check if user is in database
            if int(userid) == int(row[0]):
                balance = row[1]
                print("old user")
                print(deposit)
                deposit = int(deposit) * 100
                print(deposit)
                balance = int(row[1]) + int(deposit)
                print(balance)
                hit = [int(interaction.user.id), balance]
        #If they are, Update Records
        if userid == hit[0]:
            cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
            con.commit()
            await interaction.response.send_message(f"Your balance is {balance}:coin:")
            log = open("log.txt", "a")
            log.writelines(f"\n{interaction.user.id} Deposited {deposit} DB {str(datetime.datetime.now())}")
            log.close()
        #If not, Create Records
        else:
            deposit = deposit * 100
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0 + int(deposit)})")
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Your balance is {0 + int(deposit)}:coin:")
    else:
        await interaction.response.send_message(f"Please Enter a Valid Ticker (T4)")            
    con.close()
##############################################################################################################################################################

@client.tree.command(name = "withdraw")
@app_commands.describe(ticker = "Ticker", withdraw = "Amount to Withdaw")
async def withdraw(interaction: discord.Interaction, ticker: str, withdraw: int):
    con = sqlite3.connect(database)
    cur = con.cursor()
    try:
        ticker.lower()
    except:
        await interaction.response.send_message(f"Please Enter a Valid Ticker (T3) ")
    if ticker == "c":
        userid = interaction.user.id
        hit = [0,0]
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
            #Check if user is in database
            if int(userid) == int(row[0]):
                balance = row[1]
                print("old user")
                balance = int(balance) - int(withdraw)
                hit = [int(interaction.user.id), balance]
        #If they are, Update Records
        if userid == hit[0]:
            if balance >= withdraw:
                cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
                con.commit()
                await interaction.response.send_message(f"Your balance is {balance}:coin:")
                log = open("log.txt", "a")
                log.writelines(f"\n{interaction.user.id} Withdrew {withdraw} C {str(datetime.datetime.now())}")
                log.close()
            else:
                await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!")
        #If not, Create Records
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!")
    elif ticker == "db":
        userid = interaction.user.id
        hit = [0,0]
        for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):

            #Check if user is in database
            if int(userid) == int(row[0]):
                balance = row[1]
                print("old user")
                withdraw = withdraw * 100
                balance = int(balance) - int(withdraw)
                hit = [int(interaction.user.id), balance]
        #If they are, Update Records
        if userid == hit[0]:
            if balance >= withdraw:
                cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
                con.commit()
                await interaction.response.send_message(f"Your balance is {balance}:coin:")
                log = open("log.txt", "a")
                log.writelines(f"\n{interaction.user.id} Withdrew {withdraw} DB {str(datetime.datetime.now())}")
                log.close()
            else:
                await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!")
        #If not, Create Records
        else:
            cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
            con.commit()
            print(f"new user {userid}")
            await interaction.response.send_message(f"Not enough :coin: in your account to Withdraw!")
    else:
        await interaction.response.send_message(f"Please Enter a Valid Ticker (T4)")            
    con.close()        

#####################################################################################################################################

@client.tree.command()
async def cbalance(interaction: discord.Interaction):
    con = sqlite3.connect(database)
    cur = con.cursor()
    hit = [0,0]
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):
        if interaction.user.id == row[0]:
            balance = row[1]
            hit = [interaction.user.id, balance]
    if interaction.user.id in hit:
        await interaction.response.send_message(f"Your balance is {balance}:coin:")
    else:
        cur.execute(f"INSERT INTO coins VALUES ({interaction.user.id}, {int(0)})")           
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
    userid = interaction.user.id    
    for row in cur.execute("SELECT name, balance FROM coins ORDER BY balance"):

        #Check if user is in database
        if int(userid) == int(row[0]):
            balance = row[1]
            print("old user")
            hit = [userid, balance]
        if int(Botid) == int(row[0]):
            botBal = int(row[1])
            print(botBal)
    if userid == hit[0]:
        if balance >= bet:
            newbalance = balance - bet
            #Remove bet from betters account
            cur.execute(f"UPDATE coins SET balance = {newbalance} WHERE name = {hit[0]}")
            con.commit()
            if botBal > winnings:
                newbal = balance - bet
                cur.execute(f"UPDATE coins SET balance = {newbal} WHERE name = {userid}")
                con.commit()
                dice = random.randint(0,100)
                if dice < doubleWinRate:
                    balance = balance + int(winnings * 0.98)
                    botBal = botBal - int(winnings * 0.98)
                    cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
                    cur.execute(f"UPDATE coins SET balance = {botBal} WHERE name = {Botid}")
                    con.commit()
                    await interaction.response.send_message(f"You won! Your balance is {balance}:coin:")
                    log = open("log.txt", "a")
                    log.writelines(f"\nDouble Or Nothing Won By {interaction.user.mention} with a Value of {winnings} {str(datetime.datetime.now())}")
#                    log.writelines(f"\nBot won {int(int(bet*2)-winnings)} {str(datetime.datetime.now())}")
                    log.close()
                else:
                    botBal = botBal + int(winnings)
                    cur.execute(f"UPDATE coins SET balance = {botBal} WHERE name = {Botid}")
                    con.commit()
                    await interaction.response.send_message(f"The house has won. Better luck next time!")
                    log = open("log.txt", "a")
                    log.writelines(f"\nDouble Or Nothing Won By Bot with a Value of {winnings} {str(datetime.datetime.now())}")
                    log.close()
            else:
                await interaction.response.send_message(f"Bot does not have enough :coin: for this action!") 
        else:
            await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")

    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
        con.commit()
        print(f"new user {userid}")
        await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")
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
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {bet} from {oldnameid} {str(datetime.datetime.now())}")
                        log.close()
                    else:
                        bet1 = winnings * 0.99
                        round(bet1)
                        balance = bet1 + hit[1]
                        cur.execute(f"UPDATE coins SET balance = {balance} WHERE name = {userid}")
                        con.commit()
                        await interaction.response.send_message(f"@{userid} Has won the Double or Nothing worth {bet} :coin:")
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {bet} from {oldnameid} {str(datetime.datetime.now())}")
                        log.close()
                else:
                    cur.execute(f"INSERT INTO games VALUES ({userid}, {bet})")
                    con.commit()
                    await interaction.response.send_message(f"Created a Coinflip with a bet of {bet}:coin:. To cancel do /coinflipcancel {bet}")
                    log = open("log.txt", "a")
                    log.writelines(f"\nCoinflip Created By {interaction.user.mention} with a Value of {bet} {str(datetime.datetime.now())}")
                    log.close()
        else:
            await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")
    else:                         
        cur.execute(f"INSERT INTO coins VALUES ({int(userid)}, {0})")
        con.commit()
        print(f"new user {userid}")
        await interaction.response.send_message(f"Not enough :coin: in your account! Use /deposit")
    con.close()
#####################################################################################################################################

## Coinflip delete
@client.tree.command(name = "coinflipdelete")
@app_commands.describe(bet = "Coinflip Amount")
async def coinflip(interaction: discord.Interaction, bet: int):
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
                log = open("log.txt", "a")
                log.writelines(f"\nCoinflip Deleted by {interaction.user.mention} with a Value of {bet} {str(datetime.datetime.now())}")
                log.close()
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
