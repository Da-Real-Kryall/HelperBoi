import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"looptoggle":{
        "aliases":["looptoggle", "loop", "repeat"],
        "syntax":"",
        "usage":"Toggles looping of the current song.",
        "category":"voice"
    }})
    @commands.command(name="looptoggle", aliases=["loop", "repeat"])
    async def _looptoggle(ctx):
        if not await Bot.ensure_voice(ctx):
            return
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        player.set_repeat(not player.repeat)
        if player.repeat:
            embed_title = f"Enabled looping."
        else:
            embed_title = f"Disabled looping."
        repeat_embed = discord.Embed(title=embed_title, colour=general_utils.Colours.red)
        await ctx.send(embed=repeat_embed)
    Bot.add_command(_looptoggle)