import discord, lavalink, re
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"connect":{
        "aliases":["connect", "joinvoice"],
        "syntax":"",
        "usage":"Connects the bot to the current voice channel.",
        "category":"voice"
    }})
    @commands.command(name="connect", aliases=["joinvoice"])
    async def _connect(ctx):
        guilds = [client for client in Bot.voice_clients if client.guild.id == ctx.guild.id]
        if len(guilds) == 0:
            if not await Bot.ensure_voice(ctx):
                return
            await ctx.send(embed=discord.Embed(title=f"Joined #{ctx.author.voice.channel.name}.", colour=general_utils.Colours.red))
        else:
            await ctx.send(embed=discord.Embed(title=f"Already connected to #{ctx.author.voice.channel.name}.", colour=general_utils.Colours.red))

    Bot.add_command(_connect)