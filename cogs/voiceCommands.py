import discord
from discord.ext import commands

import os
import yt_dlp
import asyncio
import youtube_dl


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def endSong(self, guild, path):
        os.remove(path)

    @commands.command(name="summon", help="Makes bot join vc")
    async def join_voice(self, ctx):
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            return True
        return False

    @commands.command(name="unsummon", help="Makes bot leave vc")
    async def leave_voice(self, ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()

    @commands.command(name="mute", aliases=["m", "M"], help="Mutes all members of vc user is in")
    @commands.has_role("Bot")
    async def mute(self, ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=True)

    @commands.command(name="unmute", aliases=["u", "U"], help="Unmutes all members of vc user is in")
    @commands.has_role("Bot")
    async def mute(self, ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)


async def setup(bot):
    await bot.add_cog(VoiceCog(bot))
