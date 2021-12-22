import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cards_info":{
        "aliases":["cards_info"],
        "syntax":"",
        "usage":"Gives info about the cards-against-humanities/helperboi system and how to use it.",
        "category":"cah"
    }})
    @commands.command(name="cards_info")
    async def _cards_info(ctx):
        info_string = """An explanation of Cards-against-(humanities/helperboi i still cant decide): (this was taken from [this website] as i cant explain things very concisely.)
        
The game's idea is simple- one player reads the question/phrase on a black card, and everyone else fills in the blank with the white card they think is funniest.
In this its much more simplified; you can submit your own cards and use the `cards_random` command to generate a random combination of white cards and a black card.

The ability to add cards is likely temporary, though once it is inevitably removed because we cannot have nice things, you can try submit cards through the `suggest` command.

Also, some cards or combination of cards might be a bit taboo, but very few should be actually NSFW, though still keep that in mind before using it.
        
Also also, when submitting black cards you only need __one__ underscore (_) to mark one place of insertion for white cards."""

        card_embed = discord.Embed(title="CAH Info:", description=info_string)
        card_embed = general_utils.format_embed(ctx.author, card_embed)

        await ctx.send(embed=card_embed)

    Bot.add_command(_cards_info)