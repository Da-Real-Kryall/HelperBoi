import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"echo":{
        "aliases":["echo"],
        "syntax":"<text>",
        "usage":"Makes the bot say the given text",
        "category":"hidden"
    }})
    @commands.is_owner()
    @commands.command(name="echo")
    async def _echo(ctx, *, content):
        await ctx.message.delete()
        await ctx.send(content)
    Bot.add_command(_echo)