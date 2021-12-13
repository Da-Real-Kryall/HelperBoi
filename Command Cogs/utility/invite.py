import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"invite":{
        "aliases":["invite"],
        "syntax":"",
        "usage":f"Returns the invite link for adding the bot to servers.",
        "category":"utility"
    }})
    @commands.command(name="invite")
    async def _invite(ctx):
        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title="Here!", description="Use this to invite the bot to servers.", url="https://discord.com/api/oauth2/authorize?client_id=849543878059098144&permissions=416578137154&scope=bot")))
    Bot.add_command(_invite)