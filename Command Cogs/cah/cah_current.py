import discord, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cah_current":{
        "aliases":["cah_current", "cah_leaderboard"],
        "syntax":"",
        "usage":"Returns info about the current cah game you are playing.",
        "category":"cah"
    }})
    @commands.command(name="cah_current", aliases=["cah_leaderboard"])
    async def _cah_current(ctx):
        try:
            info = Bot.cah.get_cah_info(ctx.author.id)
        except Bot.cah.errors.NotInAGame:
            await ctx.send(embed=general_utils.error_embed(True, f"You are not currently in a game."))
            return
        info_embed = discord.Embed(title=f"You are in game `{info['key']}`, here is the leaderboard:", description=f"The game state is `{info['state']}`.")
        info_embed.add_field(name="Leaderboard:", value=info['leaderboard'])
        info_embed = general_utils.format_embed(ctx.author, info_embed, "charcoal")
        await ctx.send(embed=info_embed)
    Bot.add_command(_cah_current)