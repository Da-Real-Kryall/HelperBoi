import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cah_addblack":{
        "aliases":["cah_addblack", "black"],
        "syntax":"[black card]",
        "usage":"Adds a new black card to the cards-against-humanity database. make sure to only use ONE underscore (_) to mark where white cards should be inserted.",
        "category":"cah"
    }})
    @commands.command(name="cah_addblack", aliases=["addblack"])
    async def _cah_addblack(ctx, *, black_card):
        card_ids = database_utils.alter_cards("black", {"insert": [(black_card, ctx.author.id)], "delete": []})

        card_embed = discord.Embed(title="Black card added!", description=black_card.replace('_', '\_'))
        card_embed = general_utils.format_embed(ctx.author, card_embed)

        await ctx.send(embed=card_embed)

    Bot.add_command(_cah_addblack)