import os
import discord
from discord.ext import commands
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from pydub import AudioSegment
from pydub.playback import play
import requests
import io

load_dotenv()

clientId = os.environ["SPOTIPY_CLIENT_ID"]
clientSecret = os.environ["SPOTIPY_CLIENT_SECRET"]
redirectUri = os.environ["SPOTIPY_REDIRECT_URI"]
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUri
    )
)


class spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.isPlaying = False
        self.isPaused = False
        self.songQueue = []
        self.ffmpegOptions = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_dalay_max 5",
            "options": "-vn",
        }
        self.vc = None

    async def playSong(self):
        if len(self.songQueue) > 0:
            self.isPlaying = True

    @commands.command(name="play", aliases=["p"], help="Toca música do spotify")
    async def play(self, ctx, *args):
        voiceChannel = ctx.author.voice.channel
        if voiceChannel == None:
            await ctx.send("Entra numa call ae bocó")

        else:
            results = sp.search(q=args, type="track")
            track = results["tracks"]["items"][0]
            trackUrl = track["external_urls"]["spotify"]
            info = {"source": trackUrl, "title": track["name"]}
            response = requests.get(trackUrl)
            sound = AudioSegment.from_file(io.BytesIO(response.content), format="wav")

            await ctx.send(
                f'Tocando agora: {track["name"]} - {track["artists"][0]["name"]}\nURL: {trackUrl}'
            )
            self.vc = await voiceChannel.connect()
            # self.vc.play(discord.FFmpegPCMAudio(play(sound), **self.ffmpegOptions))
            self.vc.play(play(sound))
            self.songQueue.append([trackUrl, voiceChannel])

    @commands.command(name="join")
    async def join(self, ctx):
        voice = ctx.author.voice.channel
        if voice == None:
            await ctx.send("cant do nothing")
        else:
            await self.vc.connect()
