import discord
from discord.ext import commands


def encrypt(type, text, key):
    texta = ""
    text = tuple(text)
    if " " in text:
        for i in text:
            texta += i
    else:
        for i in text:
            texta += i + " "
    text = texta
    cypher = ""
    if type == "encrypt":
        for letter in text:
            cypher += chr(ord(letter) + int(key))
        return cypher
    elif type == "decrypt":
        for letter in text:
            cypher += chr(ord(letter) - int(key))
        return cypher
    else:
        return "An error occured"


def fibonacci(x):
    x = int(x)
    a = 0
    b = 1
    count = 0
    while count <= x-3:
        c = a + b
        a = b
        b = c
        count += 1
    return b


def mass_generator(formula):
    mass = 0
    periodic_table = {"H": 1,
                      "He": 4,
                      "Li": 7,
                      "Be": 9,
                      "B": 11,
                      "C": 12,
                      "N": 14,
                      "O": 16,
                      "F": 19,
                      "Ne": 20,
                      "Na": 23,
                      "Mg": 24,
                      "Al": 27,
                      "Si": 28,
                      "P": 31,
                      "S": 32,
                      "Cl": 35.5,
                      "Ar": 40,
                      "K": 39,
                      "Ca": 40,
                      "Sc": 45,
                      "Ti": 48,
                      "V": 51,
                      "Cr": 52,
                      "Mn": 55,
                      "Fe": 56,
                      "Co": 59,
                      "Ni": 59,
                      "Cu": 63.5,
                      "Zn": 65,
                      "Ga": 70,
                      "Ge": 73,
                      "As": 75,
                      "Se": 79,
                      "Br": 80,
                      "Kr": 84}
    element = formula
    elements = []
    coeffecients = []

    for i in element:
        elements.append(i)

    index = 0
    x = elements
    for i in x:
        try:
            i = int(i)  # If i is an integer, do nothing
        except:
            try:
                # If the value after i is an integer, do nothing
                int(elements[index+1])
            except:
                # If the two values aren't integers, insert a 1
                elements.insert(index+2, 1)
        index += 1
    index = 0
    for i in elements:
        try:
            i = int(i)
            try:
                int(elements[index+i])
                coeffecients.append(int(str(i)+str(elements[index+i])))
                elements.pop(index+1)
                elements.pop(index)
            except:
                coeffecients.append(i)
                elements.pop(index)

        except:
            pass
        index += 1

    index = 0
    for i in elements:
        try:
            if elements[index+1] == elements[index+1].lower():
                elements[index] = i+elements[index+1]+" "
            else:
                elements[index] = elements[index] + " "
        except:
            pass
        index += 1

    index = 0
    for i in elements:
        try:
            if i == i.lower():
                elements.pop(index)
            index += 1
        except:
            pass

    element = ""
    try:
        for i in elements:
            element += i
        element = element.split(" ")
    except:
        pass

    for i in range(len(element)):
        mass += periodic_table[element[i]] * coeffecients[i]
    return mass


class customCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="molar_mass", help="Calculates the molar mass of formulas, work in progress")
    async def molar_mass(self, ctx, arg):
        x = str("<@" + str(ctx.author.id) + ">" + " the molar mass of " +
                arg + " is " + str(mass_generator(arg)))

        await ctx.send(x)

    @commands.command(name="encrypt",
                      help="Encrypts the first argument with a key (second argument). Also called basic Caesar encryption")
    async def encrypt_this(self, ctx, key, *args):
        try:
            await ctx.send(encrypt("encrypt", args, key))
        except ValueError:
            await ctx.send("I am a  computer and got an error")

    @commands.command(name="decrypt", help="Decrypts encryption done by a basic Caesar encryption")
    async def decrypt_this(self, ctx, key, *args):
        try:
            await ctx.send(encrypt("decrypt", args, key))
        except ValueError:
            await ctx.send("I am a computer and got an error")

    @commands.command(name="fibonacci", help="Returns the nth term of the Fibonacci sequence")
    async def fibonacci_(self, ctx, index):
        if int(index) <= 500:
            try:
                await ctx.send(fibonacci(index))
            except ValueError:
                await ctx.send("I am a computer and got an error")
        else:
            await ctx.send("Number too big, don't crash my computer")


async def setup(bot):
    await bot.add_cog(customCog(bot))
