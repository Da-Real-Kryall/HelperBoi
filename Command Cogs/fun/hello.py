import discord, random
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"hello":{
        "aliases":["hello", "hi", "hey"],
        "syntax":"",
        "usage":"Greetings are always polite!",
        "category":"fun"
    }})
    @commands.command(name="hello", aliases=["hi", "hey"])
    async def _hello(ctx):
        greetings = ['hoi!', 'hello', 'hey', 'hay', 'hoi', 'hewo', 'hewo!', 'hey!', 'hay!', 'hi there', 'hi there!', 'salutations', 'salutations!', 'oh hi', 'oh, hi', 'why hello there!', 'hewo dere!']
        await ctx.send(random.choice(greetings))

    Bot.add_command(_hello)
