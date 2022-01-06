import subprocess, sys, discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"restart":{
        "aliases":["restart"],
        "syntax":"",
        "usage":"Restarts the bot.",
        "category":"utility"
    }})
    @commands.is_owner()
    @commands.command(name="restart")
    async def _restart(ctx):
        await ctx.send(embed=discord.Embed(title="Reloading the bot...", colour=general_utils.Colours.green))
        subprocess.Popen(["python3", "Helpercode.py"])#["source", "/Users/codyryall/Desktop/HelperBoiRewrite/bot_env/bin/activate;", "cd", "/Users/codyryall/Desktop/Asciiartist/contents;", 
        sys.exit(0)

    Bot.add_command(_restart)