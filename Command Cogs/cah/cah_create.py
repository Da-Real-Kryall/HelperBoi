import discord, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cah_create":{
        "aliases":["cah_create"],
        "syntax":"",
        "usage":"Creates a cards-against-humanity game if you arent in one already, and tells you its id. The game starts once you run the `cah_start` command, after your friends have joined with `cah_join <game key>`.",
        "category":"cah"
    }})
    @commands.command(name="cah_create")
    async def _cah_create(ctx):
        try:
            key = Bot.cah.create_cah_session(ctx.author.id)
        except Bot.cah.errors.AlreadyInGame:
            await ctx.send(embed=general_utils.error_embed(False, f"You are already in a game! use the `cah_leave` command to leave your curent game."))
            return
        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Game created with id {key}.", description="Wait for others to join, then use the `cah_start` command to start the game."), "charcoal"))

    Bot.add_command(_cah_create)