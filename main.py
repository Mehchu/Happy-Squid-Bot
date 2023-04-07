import os
import aiohttp

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='#', intents=discord.Intents.all(),
                         description="Happy Squid Bot")
        self.initial_extensions = [
            'cogs.voiceCommands',
            'cogs.customCommands',
            'cogs.randomCommands',
            'cogs.adminCommands',
            'cogs.music'
        ]

    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
    async def background_task(self):
        pass

    async def on_ready(self):
        """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

        print(
            f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

        # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
        await bot.change_presence(activity=discord.Game(name='guess the colour of the Bugatti', type=1, url='https://twitch.tv/mehchu101'))
        print(f'Successfully logged in and booted...!')


bot = MyBot()


# Does this everytime a message is sent
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id != 783751774757716048:  # Checks if sent by bot
        # Checks if the funny numbers are in the messages
        if (" 69 " in message.content) or (" 420 " in message.content):
            await message.channel.send("Nice 👌")


bot.run(TOKEN, reconnect=True)  # Runs the bot
