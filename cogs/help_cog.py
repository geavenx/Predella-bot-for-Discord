import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.helpMessage = """
```
Comandos:
$p help - Mostra todos os comandos disponíveis
$p play <música> - Toca música do Youtube
$p queue - Mostra as próximas músicas que serão tocadas
$p skip - Pula o som atual
$p clear - apaga luz apaga tudo
$p leave - na levada quetamina eu odeio mina quieta
$p pause - Pausa o som atual
$p resume - Reproduz o som atual que tava pausado
```
"""
        self.text_channel_text = []
        
    @commands.Cog.listener()
    async def sendToALL(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)
            
    @commands.command(name='help', help='Mostra todos os comandos disponíveis')
    async def help(self, ctx):
        await ctx.send(self.helpMessage)