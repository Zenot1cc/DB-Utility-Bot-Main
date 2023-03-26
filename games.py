## Single Player Coinflip
import sqlite3
import random
import datetime
async def doubleornothing(interaction, bet, doubleWinRate, playerTakings, botTakings, database, Botid):
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
                botNewBal = botBal - bet
                cur.execute(f"UPDATE coins SET balance = {newbal} WHERE name = {userid}") # Remove Balance from Users Account
                cur.execute(f"UPDATE coins SET balance = {botNewBal} WHERE name = {Botid}") # Remove Balance from Bots Account
                con.commit()
                dice = random.randint(0,100)
                if dice < doubleWinRate:
                    balance = balance + playerTake
                    botBal = botBal - playerTake
                    cur.execute(f"UPDATE coins SET balance = {int(balance)} WHERE name = {userid}") # Add winnings to Users Account
                    cur.execute(f"UPDATE coins SET balance = {int(botBal)} WHERE name = {Botid}") # Remove Winnings from Bots Account
                    con.commit()
                    await interaction.response.send_message(f"You won! Your balance is {balance}:coin:") # Success
                    log = open("log.txt", "a")
                    log.writelines(f"\nDouble Or Nothing Won By {interaction.user.mention} with a Value of {winnings} {str(datetime.datetime.now())}")
                    log.close()
                    log = open("botGambleWinnings", "a")
                    log.writelines(f"\nBot took {int(BotTake)}")
                    log.close()
                else:
                    botBal = botBal + int(playerTake)
                    cur.execute(f"UPDATE coins SET balance = {botBal} WHERE name = {Botid}") # Add winnings to Bots Account
                    con.commit()
                    await interaction.response.send_message(f"The house has won. Better luck next time!") # Success
                    log = open("log.txt", "a")
                    log.writelines(f"\nDouble Or Nothing Won By Bot with a Value of {winnings} {str(datetime.datetime.now())}")
                    log.close()
                    log = open("botGambleWinnings", "a")
                    log.writelines(f"\nBot took {int(BotTake)}")
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
async def coinflip(interaction, bet, playerTakings, botTakings, database):
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
                        user = oldname
                        await interaction.response.send_message(f"{user.mention} Has won the Double or Nothing worth {winnings} :coin:") # Success
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {winnings} from {oldnameid} {str(datetime.datetime.now())}")
                        log.close()
                        log = open("botGambleWinnings", "a")
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
                        user = userid
                        await interaction.response.send_message(f"{user.mention} Has won the Double or Nothing worth {bet} :coin:") # Success
                        log = open("log.txt", "a")
                        log.writelines(f"\nCoinflip Played By {interaction.user.mention} with a Value of {bet} from {olduserid} {str(datetime.datetime.now())}")
                        log.close()
                        log = open("botGambleWinnings", "a")
                        log.writelines(f"\nBot took {int(botTake)}")
                        log.close()
                else:
                    cur.execute(f"INSERT INTO games VALUES ({userid}, {bet})") # Add Game to Database
                    con.commit()
                    await interaction.response.send_message(f"Created a Coinflip with a bet of {bet}:coin:. To cancel do /coinflipdelete {bet}") # Success
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
async def coinflipdelete(interaction, bet, database):
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

#####################################################################################################################################

## Coinflip list
async def coinflipList(interaction, database):
    gameListlist = []
    gameList = ""
    count = 0
    con = sqlite3.connect(database)
    cur = con.cursor()
    for row in cur.execute(f"SELECT name, bet FROM games ORDER BY bet"):
        if count < 5:
            gameListlist.append(row[1])
            gameList = gameList + "\n" + str(row[1]) + ":coin:"
    if len(gameListlist) == 0:
        await interaction.response.send_message(f"There is currently no active Coinflip Games. Use /Coinflip to make one!") # Error 
    else:
        await interaction.response.send_message(f"Current Coinflip Games: {gameList}")
