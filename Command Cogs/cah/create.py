import discord, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"create":{
        "aliases":["create"],
        "syntax":"",
        "usage":"Creates a cards-against-humanity game if you arent in one already, and tells you its id. The game starts once you run the `cah_start` command, after your friends have joined with `cah_join <game key>`.",
        "category":"cah"
    }})
    @commands.command(name="create")
    async def _create(ctx):
        try:
            key = Bot.cah.create_cah_session(ctx.author.id)
        except Bot.cah.errors.AlreadyInGame:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"You are already in a game! use the `leavegame` command to leave your curent game."))
            return
        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Game created with the key `{key}`.", description=f"Wait for others to join with `{await Bot.command_prefix(Bot, ctx.message)}joingame {key}`, then use the `start` command to start the game."), "charcoal"))

    Bot.add_command(_create)