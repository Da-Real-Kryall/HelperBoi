import discord, lavalink, re
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"current_song":{
        "aliases":["current_song", "current"],
        "syntax":"",
        "usage":"Connects the bot to the current voice channel.",
        "category":"voice"
    }})
    @commands.command(name="current_song", aliases=["current"])
    async def _current_song(ctx):
        player = Bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            await ctx.send(embed=discord.Embed(title="Not connected to a voice channel.", colour=general_utils.Colours.red))
            return
        if player.current != None:
            embed_title = f"Currently playing {player.current.title}"
        else:
            embed_title = "No songs are being played."
        current_embed = discord.Embed(title=embed_title, colour=general_utils.Colours.red)
        await ctx.send(embed=current_embed)

    Bot.add_command(_current_song)