import os
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN=os.environ['TOKEN']

""" def getPrefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)] """

# bot = discord.Client(intents= discord.Intents().all())
bot = commands.Bot(intents= discord.Intents().all(), command_prefix= '=-')

#class myBot(discord.Client):
@bot.event
async def on_ready():
    serverCounter = 0
    for guild in bot.guilds:
        print(f'- {guild.id} (name: {guild.name})')
        print('----------')
        serverCounter += 1
        
    print(f'- {bot.user} está em {serverCounter} servidores atualmente')
    print('----------')

@bot.command()
async def eutanasia(ctx):
    print('- eutanasia called')
    await ctx.send('enfermeira oriental eu tô na ásia?')

@bot.command()
async def clear(ctx):
    print('- clear called\n')
    
    

bot.run(TOKEN)