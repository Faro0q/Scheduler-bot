import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('create'):
        userMessage = message.content.split(" ")
        await message.channel.send(userMessage)

client.run('token')