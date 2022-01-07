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
        current_embed = discord.Embed(colour=general_utils.Colours.red)
        if player.current != None:
            current_embed.title = f"Currently playing:" #add progress bar
            current_embed.description = f"[{player.current.title}](https://youtu.be/{player.current.identifier})\n\nDuration is {general_utils.strf_timedelta(int(player.current.duration/1000))}.\n{general_utils.strf_timedelta(int(player.position/1000))} through. ({round(player.position/player.current.duration*100, 1)}%)"
            current_embed.set_thumbnail(url=f"https://img.youtube.com/vi/{player.current.identifier}/default.jpg")
        else:
            current_embed.title = "No songs are being played."
        await ctx.send(embed=current_embed)

    Bot.add_command(_current_song)