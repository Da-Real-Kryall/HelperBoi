import discord
from discord.ext import commands

def setup(Bot):
    Bot.command_info.update({"destroy":{
        "aliases":["destroy"],
        "syntax":"",
        "usage":"Stops the bot, only for the bot owner!",
        "category":"utility"
    }})

    @commands.is_owner()
    @commands.command(name="destroy")
    async def _destroy(ctx):
        with open("Recources/images/boom.png", "rb") as file:
            await ctx.send("Shutting down... (restarting if on service)", file=discord.File(file))
        await Bot.logout()

    Bot.add_command(_destroy)