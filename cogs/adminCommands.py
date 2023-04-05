import discord
from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", help="Sends message to given channel")
    async def announce(self, ctx, channel, *args):
        chat = self.get_channel(int(channel))
        string = ""
        if args[0][0] != ".":
            for i in args:
                string += i + " "
            await chat.send(string)

    @commands.command(name="spam",
                      help="Spams second argument in the channel id provided in the first argument, third argument amount of "
                      "times")
    async def spam(self, ctx, channel, time, *args):
        chat = self.get_channel(int(channel))
        amount = 0
        string = ""
        if args[0][0] != ".":
            for i in args:
                string += i + " "
            if int(time) <= 25:
                while amount != int(time):
                    await chat.send(string)
                    amount += 1

    @commands.command(name="kick")
    async def kick(self, ctx, member: discord.Member, *args):
        await member.kick(reason=args)
        await ctx.channel.send(f"**{member} has been kicked from this server by {ctx.author}**")

    @commands.command(name="role", help="Gives users roles")
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"The role ''**{role}**'' was just given to **{member}**")

    @commands.command(name="unrole", help="Gives users roles")
    async def unrole(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"The role ''**{role}**'' was just taken away from **{member}**")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
