import discord
from discord.ext import commands

import os
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

    @commands.command(name='play', help='To play song')
    async def play(self, ctx, url):
        data = await self.join_voice(self, ctx)
        if data == True:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                file = ydl.extract_info(url, download=True)
            guild = ctx.message.guild
            voice_client = guild.voice_client
            path = str(file['title']) + "-" + str(file['id'] + ".mp3")

            voice_client.play(discord.FFmpegPCMAudio(
                path), after=lambda x: self.endSong(guild, path))
            voice_client.source = discord.PCMVolumeTransformer(
                voice_client.source, 1)

    @commands.command(name='bugatti', help='To play song')
    async def topG(self, ctx):
        data = await self.join_voice(ctx)
        if data == True:
            guild = ctx.message.guild
            voice_client = guild.voice_client
            path = "topg.mp3"

            voice_client.play(discord.FFmpegPCMAudio(
                path), after=lambda x: repeat(guild, voice_client, discord.FFmpegPCMAudio(
                    path)))
            voice_client.source = discord.PCMVolumeTransformer(
                voice_client.source, 1)

            def repeat(guild, voice, audio):
                voice.play(audio, after=lambda e: repeat(guild, voice, audio))
                voice.is_playing()

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

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
