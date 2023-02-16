import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN=os.environ['TOKEN']

bot = commands.Bot(intents= discord.Intents().all(), command_prefix= '$')

bot.remove_command('help')
from cogs.music_cog import spotify
from cogs.help_cog import help_cog

@bot.event
async def on_ready():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(spotify(bot))
    
    serverCounter = 0
    for guild in bot.guilds:
        print(f'- {guild.id} (name: {guild.name})')
        print('----------')
        serverCounter += 1
        
    print(f'- {bot.user} está em {serverCounter} servidores atualmente')
    print('----------')

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if message.content.startswith('Mais que ela'):
        await message.reply('o Predella', mention_author= True)
    await bot.process_commands(message)

@bot.command()
async def eutanasia(ctx):
    print('- eutanasia called...')
    await ctx.send('enfermeira oriental eu tô na ásia?')

@bot.command()
async def clearC(ctx, amount:int):
    print('- clear called...')
    if amount <= 10000:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Predella matou {amount} mensagens.')
    else:
        await ctx.send(f'Calma aí meu mano o Predella é um só, {amount} é muita coisa.')

bot.run(TOKEN)