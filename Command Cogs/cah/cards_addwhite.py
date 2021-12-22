import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cards_addwhite":{
        "aliases":["cards_addwhite", "addwhite"],
        "syntax":"[white card]",
        "usage":"Adds a new white card to the cards-against-humanity database.",
        "category":"cah"
    }})
    @commands.command(name="cards_addwhite", aliases=["addwhite"])
    async def _cards_addwhite(ctx, *, white_card):
        card_ids = database_utils.alter_cards("white", {"insert": [(white_card, ctx.author.id)], "delete": []})

        card_embed = discord.Embed(title="White card added!", description=white_card)
        card_embed = general_utils.format_embed(ctx.author, card_embed)

        await ctx.send(embed=card_embed)

    Bot.add_command(_cards_addwhite)