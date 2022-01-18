import discord, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cah_leave":{
        "aliases":["cah_leave"],
        "syntax":"",
        "usage":"Makes the author leave their current Cards-Against-Humanity game.",
        "category":"cah"
    }})
    @commands.command(name="cah_leave")
    async def _cah_leave(ctx):
        try:
            key = await Bot.cah.leave_cah_game(ctx.author.id)
        except Bot.cah.errors.NotInAGame:
            await ctx.send(embed=general_utils.error_embed(False, f"You arent even in a game yet!"))
            return
        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"You have left the game with the key `{key}`."), "charcoal"))
    Bot.add_command(_cah_leave)