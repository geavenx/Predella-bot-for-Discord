import os
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.clientId = os.environ['SPOTIPY_CLIENT_ID']
        self.clientSecret = os.environ['SPOTIPY_CLIENT_SECRET']
        self.redirectUri = os.environ['SPOTIPY_REDIRECT_URI']
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.clientId, client_secret=self.clientSecret, redirect_uri=self.redirectUri))

        self.isPlaying = False
        self.isPaused = False
        
        self.songQueue = []
        
        self.youtube_dlOptions = {'format': 'bestaudio', 'noplaylist': 'True'}        
        self.ffmpegOptions = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_dalay_max 5', 'options': '-vn'}
        
        self.vc = None
        
    def searchYt(self, item):
        with YoutubeDL(self.youtube_dlOptions) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def searchSpotify(self, query):
        results = self.sp.search(q=query, type='track')
        track = results['tracks']['items'][0]
        trackUrl = track['external_urls']['spotify']
        
        return trackUrl
           
    def playNext(self):
        if len(self.songQueue) > 0:
            self.isPlaying = True
            
            m_url = self.songQueue[0][0]['source']
            self.songQueue.pop(0)
            self.vc.play(discord.FFmpegAudio(m_url, **self.ffmpegOptions), after=lambda e: self.playNext())
        else:
            self.isPlaying = False
    
    async def playMusic(self, ctx):
        if len(self.songQueue) > 0:
            self.isPlaying = True
            m_url = self.songQueue[0][0]['source']
            
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.songQueue[0][1].connect()
                
                if self.vc == None:
                    await ctx.send('Não consegui me conectar ao canal de voz')
                    return
            else:
                await self.vc.move_to(self.songQueue[0][1])
                
            self.songQueue.pop(0)
            
            self.vc.play(discord.FFmpegAudio(m_url, **self.ffmpegOptions), after=lambda e: self.playNext())
        
        else:
            self.isPlaying = False
    
    @commands.command(name='playyt', aliases=['pyt'], help='Toca música do youtube ué')
    async def playyt(self, ctx, *args):
        query = " ".join(args)
        voiceChannel = ctx.author.voice.channel
        
        if voiceChannel is None:
            await ctx.send('Entra numa call aí... Heyo men my name is predella costa gold!!')
        
        elif self.isPaused:
            self.vc.resume()
        
        else:
            song = self.searchYt(query)
            
            if type(song) == type(True):
                await ctx.send('Não consegui baixar o som, formato inválido')
            
            else:
                await ctx.send('Som adicionado na fila')
                self.songQueue.append([song, voiceChannel])
                
                if self.isPlaying == False:
                    await self.playMusic(ctx)

    @commands.command(name='play', aliases=['p'], help='Toca música do spotify ué')
    async def play(self, ctx, *args):
        query = "".join(args)
        voiceChannel = ctx.author.voice.channel
        
        if voiceChannel == None:
            await ctx.send('Entra numa call aí... Heyo men my name is predella costa gold!!')
            
        elif self.isPaused:
            self.vc.resume()
        
        else:
            song = self.searchSpotify(query)
            
            if self.isPlaying == True:
                self.songQueue.append([song, voiceChannel])
            
            else:
                await self.playMusic(ctx)
        
    @commands.command(name='pause', help='Pausa o som atual')
    async def pause(self, ctx, *args):
        if self.isPlaying:
            self.isPlaying = False
            self.isPaused = True
            self.vc.pause()
        
        elif self.isPaused:
            self.vc.resume()
        
    @commands.command(name='resume', aliases=['r'], help='Reproduz o som atual que tava pausado')
    async def pause(self, ctx, *args):
        if self.isPaused:
            self.isPlaying = True
            self.isPaused = False
            self.vc.resume()
            
    @commands.command(name='skip', aliases=['s'] ,help='Pula o som atual')
    async def pause(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.playMusic(ctx)
            
    @commands.command(name='queue', aliases=['q'], help='Mostra as próximas músicas que serão tocadas')
    async def queue(self, ctx):
        queueList = ''
        for i in range(0, len(self.songQueue)):
            if i > 4: break
            queueList += self.songQueue[i][0]['title'] + '\n'
        
        if queueList != '':
            await ctx.send(queueList)
            
        else:
            await ctx.send('Não tem nada na fila bocó')

    @commands.command(name='clear', aliases=['ls'], help='apaga luz apaga tudo')
    async def clear(self, ctx, *args):
        if self.vc != None and self.isPlaying:
            self.vc.stop()
        self.songQueue = []
        await ctx.send('A fila ta limpa, bota um costa gold ae agora')
        
    @commands.command(name='leave', aliases=['l'], help='na levada quetamina eu odeio mina quieta')
    async def dc(self, ctx):
        self.isPlaying = False
        self.isPaused = False
        await self.vc.disconnect()