import discord
from discord.ext import commands
import random
import asyncio
import numpy as np

def joke():
    import random
    jokes = {"I've invented a new word!": "Plagiarism!",
             "Did you hear about the mathematician who’s afraid of negative numbers?": "He’ll stop at nothing to avoid them.",
             "Why do we tell actors to “break a leg?”": "Because every play has a cast.",
             "Helvetica and Times New Roman walk into a bar.": "”Get out of here!” shouts the bartender. “We don’t serve your type.”",
             "A woman in labor suddenly shouted, ”Shouldn’t! Wouldn’t! Couldn’t! Didn’t! Can’t!”": "”Don’t worry,” said the doc. “Those are just contractions.”",
             "Why is Micheal Jackson bad at chess?": "Because he's dead.",
             "Why is it impossible to solve a murder in Alabama?": "Because they all have the same DNA."}
    punchlines = []
    for i in jokes:
        punchlines.append(i)
    choice = random.choice(punchlines)
    array = []
    array.append(choice)
    array.append(jokes[choice])
    return array


class RandomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll',
                      help='Returns a random number between 1 and the argument you give it. For example .roll 10 will give a '
                      'number between 1 and 10')
    async def randomness(self, ctx, arg):
        try:
            await ctx.send(random.randint(1, int(arg)))
        except ValueError:
            await ctx.send("Enter an integer please")

    @commands.command(name="rock_paper_scissors", help="Plays a game of rock paper scissors")
    async def rock_paper_scissors(self, ctx, player):
        computer = random.randint(1, 3)
        values = {"rock": 1,
                  "paper": 2,
                  "scissors": 3}
        value = {1: "rock",
                 2: "paper",
                 3: "scissors"}
        if player not in values:
            await ctx.send("Please enter rock, paper or scissors next time")
        elif values[player.lower()] == computer:
            await ctx.send("It is a draw, I played {}".format(value[computer]))
        elif values[player.lower()] == computer + 1 or (values[player.lower()] == 1 and computer == 3):
            await ctx.send("You win, I played {}".format(value[computer]))
        else:
            await ctx.send("I win, I played {}".format(value[computer]))

    @commands.command(name="flip", help="Flips a coin")
    async def spam(self, ctx):
        flip = random.randint(1, 2)
        if flip == 1:
            await ctx.send("Heads!")
        else:
            await ctx.send("Tails!")

    @commands.command(name="poll", help="State the channel id then provide up to 5 arguments to be options for the poll")
    async def poll(self, ctx, atitle, channel, *args):
        embed = discord.Embed(title=atitle,
                              description="Choose an option by reacting with the corresponding emoji")

        emojis = {1: "1️⃣",
                  2: "2️⃣",
                  3: "3️⃣",
                  4: "4️⃣",
                  5: "5️⃣",
                  6: "6️⃣"}
        chat = self.get_channel(int(channel))
        array = [[], [], [], [], [], []]
        index2 = 0
        for i in args:
            if i != ".":
                array[index2].append(i)
            else:
                index2 += 1
        for i in array:
            if array[-1] == []:
                array.pop()
        if array[-1] == []:
            array.pop()
        string = ""
        for i in range(len(array)):
            for j in array[i]:
                string += j + " "
            array[i] = string
            string = ""
        counter = 1
        string = ""
        languages = ["css", "yaml", "fix", "prolog", "ml"]
        for choice in array:
            language = languages[random.randint(0, 4)]
            choice = str(f"""```{language}\n{choice}```""")
            embed.add_field(name=emojis[counter], value=choice)
            counter += 1
        msg = await chat.send(string, embed=embed)
        counter = 1
        for i in array:
            await msg.add_reaction(emojis[counter])
            counter += 1

    @commands.command(name="joke", help="Tells a random joke")
    async def joking(self, ctx):
        messages = joke()
        await ctx.send(messages[0])
        await asyncio.sleep(3)
        await ctx.send(messages[1])

    @commands.command(name="choose", description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        await ctx.send(random.choice(choices))


async def setup(bot):
    await bot.add_cog(RandomCog(bot))
