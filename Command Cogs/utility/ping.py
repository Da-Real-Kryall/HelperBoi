import discord, time
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"ping":{
        "aliases":["ping", "latency"],
        "syntax":"",
        "usage":"Returns the bot latency",
        "category":"utility"
    }})
    @commands.is_owner()
    @commands.command(name="ping", aliases=["latency"])
    async def _ping(ctx):

        embed1 = discord.Embed(title="Pinging...", description="You should only see this message for a moment.")
        embed1 = general_utils.format_embed(ctx.author, embed1, "yellow")

        before = time.monotonic()
        message = await ctx.send(embed=embed1)

        ping = round((time.monotonic()-before)*1000,1)
        embed2 = discord.Embed(title=":ping_pong: Pong and all that.", description=f"Latency: {ping}ms\nAPI Latency: {round(Bot.latency * 1000, 1)}ms")
        embed2 = general_utils.format_embed(ctx.author, embed2, "green")

        await message.edit(embed=embed2)

    Bot.add_command(_ping)
