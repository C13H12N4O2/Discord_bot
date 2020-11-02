import discord
import utils
import asyncio
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_state = None
        self.tail = None
        self.path = './Youtube'
        self.loop = asyncio.get_event_loop()
    
    @commands.command(name='이리와')
    async def _join(self, ctx):
        target = ctx.author.voice.channel
        self.voice_state = await target.connect()
    
    @commands.command(name='기다려')
    async def _stop(self, ctx):
        self.voice_state.stop()
        
    @commands.command(name='움직여')
    async def _resume(self, ctx):
        self.voice_state.resume()

    @commands.command(name='돌아가')
    async def _leave(self, ctx):
        if not self.voice_state:
            self.voice_state = await ctx.me.voice.channel.connect()
        self.voice_state.stop()
        await self.voice_state.disconnect()
    
    @commands.command(name='노래해')
    async def _play(self, ctx, url):
        if not self.voice_state:
            self.voice_state = await ctx.me.voice.channel.connect()
        if not self.voice_state.is_playing():
            mp3_path = utils.download_youtube(self.path, url)
            self.tail = await self.voice_state.play(utils.play_music(mp3_path))

    async def _next(self, ctx, url):
        loop.run_until_complete(self.voice_state.is_palying())
        loop.close()
        self._play(ctx, url)
