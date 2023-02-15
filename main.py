import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN=os.environ['TOKEN']

bot = commands.Bot(intents= discord.Intents().all(), command_prefix= '$p ')

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
    print('- eutanasia called...')
    await ctx.send('enfermeira oriental eu tô na ásia?')

@bot.command()
async def clear(ctx, amount:int):
    print('- clear called...')
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Predella matou {amount} mensagens.')
    
bot.run(TOKEN)