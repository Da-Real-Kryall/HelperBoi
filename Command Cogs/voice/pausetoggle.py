import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"pausetoggle":{
        "aliases":["pausetoggle", "pause"],
        "syntax":"<song>",
        "usage":"Used to toggle pause/play for the current song.",
        "category":"voice"
    }})
    @commands.command(name="pausetoggle", aliases=["pause"])
    async def _pausetoggle(ctx):
        await Bot.ensure_voice(ctx)
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        if player.paused == False:
            await player.set_pause(True)
            await ctx.send(embed=discord.Embed(title=":pause_button:  Pausing the current song.", colour=general_utils.Colours.red))
        else:
            await player.set_pause(False)
            await ctx.send(embed=discord.Embed(title=":arrow_forward:  Resuming the current song.", colour=general_utils.Colours.red))
    Bot.add_command(_pausetoggle)