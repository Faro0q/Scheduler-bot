import discord
import os
import re 
from datetime import datetime, time, timedelta
from dotenv import load_dotenv
import requests


EVENTS = []
COUNT = 1
load_dotenv()
client = discord.Client()
BLOCKED_IDS = [139981655019487232] #kevin
ANNOUNCEMENTS = []

def formatChecker(msg):
    # Correct:
    # create Valorant 03/02 09:00 @gello

    if(len(msg) < 4):
        return "Incorrect format. Type 'event help' to see the correct format."

    date = msg[2]
    time = msg[3]
    dateReg = re.search("^(0?[1-9]|1[012])/[1-2][0-9]|30|31|[0][1-9]$", date) # Check if date is valid
    timeReg = re.search("^(0[1-9]|1[0-9]|2[0123]):[0-5][0-9]$", time) # Check if time is valid
    
    if not (dateReg):
        return "Incorrect date format. Type 'event help' to see the correct format."
    if not (timeReg):
        return "Incorrect time format. Type 'event help' to see the correct format."
    else:
        return ""

def increment():
    global COUNT
    COUNT = COUNT+1

def newEvent(msg, author):
    # create csgo 9:00 @someone
    newEvent = ""
    for x in range(1, len(msg)):
        newEvent += msg[x] + " "
    
    event = "**" + newEvent.strip() + "**"
    author = "**" + str(author) + "**"
    EVENTS.append(str(COUNT) + ". " + event + " created by: " + author)
    increment()
    print(EVENTS)

def blockedUsers(message):
    return "Go f yourself"

def getInsults():
    return requests.get("https://insult.mattbas.org/api/insult").text

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('insult'):
        userMessage = message.content.split(" ")
        if "<@130824291787735040>" in userMessage:
            return await message.channel.send("Can't insult Daddy 😘")

        usersInsulted = ""
        if(len(userMessage) > 1):
            for x in userMessage[1:]:
                usersInsulted += x + " "
            
        await message.channel.send(usersInsulted.strip() + "  " + getInsults())

    # date_time_str = datetime.now().strftime("%m/%d %H:%M")
    
    if message.content.startswith('create'):
        if message.author.id in BLOCKED_IDS:
            return await message.channel.send(blockedUsers(message))

        userMessage = message.content.split(" ")
        wrongFormat = formatChecker(userMessage)
        if(wrongFormat):
            await message.channel.send(wrongFormat)
        else:
            newEvent(userMessage, message.author)
            await message.channel.send("Event added! Type 'events' to list all the events")

    if message.content.startswith('events'):
        if message.author.id in BLOCKED_IDS:
            return await message.channel.send(blockedUsers(message))
        if(len(EVENTS) == 0):
            await message.channel.send("No events")
        else:
            # output = globalCount + 
            await message.channel.send('Events:\n')
            for x in EVENTS:
                await message.channel.send(str(x))
    
    if message.content.startswith('event help'):
        if message.author.id in BLOCKED_IDS:
            return await message.channel.send(blockedUsers(message))
        await message.channel.send("To create an event, please use this format:\n `create CSGO 06/08 09:00 @csnerd`")

    if message.author not in ANNOUNCEMENTS:
        ANNOUNCEMENTS.append(message.author)
        await message.channel.send("Do you have $1? <@"+str(message.author.id)+"> Buy this shit dumbass \n https://www.humblebundle.com/games/capcom-summer-2022-bundle")


client.run(os.getenv('token'))