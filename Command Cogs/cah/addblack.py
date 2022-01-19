import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"addblack":{
        "aliases":["addblack"],
        "syntax":"[black card]",
        "usage":"Adds a suggestion for a new black card to be added to the cards-against-humanity database. make sure to only use ONE underscore (_) to mark where white cards should be inserted.",
        "category":"cah"
    }})
    @commands.command(name="addblack")
    async def _addblack(ctx, *, black_card):
        info = await Bot.application_info()
        owner = info.owner
        if ctx.author == owner:
            card_ids = database_utils.alter_cards("black", {"insert": [(black_card, ctx.author.id)], "delete": []})

            card_embed = discord.Embed(title="Black card added!", description=black_card.replace('_', '\_'))
        else:
            await owner.send(f"{ctx.author} has suggested a black card:\n`{black_card}`")
            card_embed = discord.Embed(title="Black card suggested!", description=f"`{black_card}`")
            database_utils.alter_suggestions({"insert":{ctx.author.id: f"(Black card suggestion) \"{black_card}\""},"delete":[]})


        card_embed = general_utils.format_embed(ctx.author, card_embed)

        await ctx.send(embed=card_embed)

    Bot.add_command(_addblack)