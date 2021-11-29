import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"e":{
        "aliases":["e"],
        "syntax":"",
        "usage":"Test command, will make E",
        "category":"fun"
    }})
    @commands.command(name="e")
    async def _e(ctx):
        e,n='E'*5,'\n'
        await ctx.send(embed=discord.Embed(title=((e*3+n)*2+(e+n)*2)*2+(e*3+n)*2,colour=general_utils.Colours.main))

    Bot.add_command(_e)