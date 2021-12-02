import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"prefix":{
        "aliases":["prefix", "get_prefix"],
        "syntax":"",
        "usage":"Returns the bot's default prefix as well as the one set in the current guild.",
        "category":"utility"
    }})

    @commands.command(name="prefix", aliases=["get_prefix"])
    async def _prefix(ctx):
        current_prefix = await Bot.get_prefix(ctx)
        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"My prefix in this server is `{current_prefix}`, "+("which is also my default prefix" if current_prefix == Bot.default_prefix else f"my default prefix is `{Bot.default_prefix}`"))))
        
    Bot.add_command(_prefix)
