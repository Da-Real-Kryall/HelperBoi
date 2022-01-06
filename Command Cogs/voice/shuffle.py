import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"shuffle":{
        "aliases":["shuffle"],
        "syntax":"",
        "usage":"Toggles queue shuffle.",
        "category":"voice"
    }})
    @commands.command(name="shuffle")
    async def _shuffle(ctx):
        await Bot.ensure_voice(ctx)
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        player.set_shuffle(not player.shuffle)
        if player.shuffle:
            embed_title = f"Enabled shuffle."
        else:
            embed_title = f"Disabled shuffle."
        shuffle_embed = discord.Embed(title=embed_title, colour=general_utils.Colours.red)
        await ctx.send(embed=shuffle_embed)
    Bot.add_command(_shuffle)