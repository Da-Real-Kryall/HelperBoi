import random
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"meme":{
        "aliases":["meme"],
        "syntax":"",
        "usage":"Aids in meme finding",
        "category":"fun"
    }})
    @commands.command(name="meme")
    async def _meme(ctx):
        if random.randint(1, 40) == 20:
            await ctx.send("me xDxDxDxD")
        else:
            await ctx.send("just use reddit smh")
        
    Bot.add_command(_meme)
