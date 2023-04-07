import discord
from discord.ext import commands

import os
import yt_dlp

yt_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def endSong(guild, path):
    os.remove(path)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx, url):
        if not ctx.message.author.voice:
            await ctx.send('you are not connected to a voice channel')
            return

        else:
            channel = ctx.message.author.voice.channel

        voice_client = await channel.connect()

        guild = ctx.message.guild

        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            path = str(file['title']) + " [" + str(file['id'] + "].mp3")
            print(path)

        voice_client.play(discord.FFmpegPCMAudio(
            path), after=lambda x: endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(
            voice_client.source, 1)

        await ctx.send(f'**Music: **{url}')
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
