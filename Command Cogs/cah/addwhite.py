import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"addwhite":{
        "aliases":["addwhite"],
        "syntax":"[white card]",
        "usage":"Adds a suggestion for a new white card to be added the cards-against-humanity database.",
        "category":"cah"
    }})
    @commands.command(name="addwhite")
    async def _addwhite(ctx, *, white_card):
        if "_" in white_card:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"You can only have white card insertion points (underscores, '_') in black cards, not white ones."))
            return
        info = await Bot.application_info()
        owner = info.owner
        if ctx.author == owner:
            card_ids = database_utils.alter_cards("white", {"insert": [(white_card, ctx.author.id)], "delete": []})

            card_embed = discord.Embed(title="White card added!", description=white_card)
        else:
            await owner.send(f"{ctx.author} has suggested a white card:\n`{white_card}`")
            card_embed = discord.Embed(title="White card suggested!", description=f"`{white_card}`")
            database_utils.alter_suggestions({"insert":{ctx.author.id: f"(White card suggestion) \"{white_card}\""},"delete":[]})


        card_embed = general_utils.format_embed(ctx.author, card_embed)

        await ctx.send(embed=card_embed)

    Bot.add_command(_addwhite)