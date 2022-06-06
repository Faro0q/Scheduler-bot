import discord
import os
import re 
from datetime import datetime, time, timedelta
from dotenv import load_dotenv


EVENTS = []
COUNT = 1
load_dotenv()
client = discord.Client()

def formatChecker(msg):
    # Correct:
    # create Valorant 03/02 09:00 @gello
    date = msg[2]
    time = msg[3]
    dateReg = re.search("^(0?[1-9]|1[012])/[1-2][0-9]|30|31|[0][1-9]$", date) # Check if date is valid
    timeReg = re.search("^(0[1-9]|1[0-9]|2[0123]):[0-5][0-9]$", time) # Check if time is valid

    if(len(msg) < 4):
        return False
    if(dateReg):
        return False
    if(timeReg):
        return False
    else:
        return True

def increment():
    global COUNT
    COUNT = COUNT+1

def scheduling(msg):
    # create csgo 9:00 @someone
    event = ""
    for x in range(1, len(msg)):
        event += msg[x] + " "
    
    EVENTS.append(str(COUNT) + ". " + event.strip())
    increment()
    print(EVENTS)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    date_time_str = datetime.now().strftime("%m/%d %H:%M ")

    await message.channel.send(date_time_str)

    if message.content.startswith('create'):
        userMessage = message.content.split(" ")
        print(userMessage)
        isFormatted = formatChecker(userMessage)
        if(isFormatted):
            scheduling(userMessage)
            await message.channel.send("Event added! Type 'events' to list all the events")
        else:
            await message.channel.send("Please input the correct format")

    if message.content.startswith('events'):
        if(len(EVENTS) == 0):
            await message.channel.send("No events")
        else:
            # output = globalCount + 
            await message.channel.send('Events:\n')
            for x in EVENTS:
                await message.channel.send(str(x))

client.run(os.getenv('token'))