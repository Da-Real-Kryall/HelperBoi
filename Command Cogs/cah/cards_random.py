import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cards_random":{
        "aliases":["cards_random", "rand"],
        "syntax":"[forced black card]",
        "usage":"Returns a random combination of the currently uploaded white and black cards",
        "category":"cah"
    }})
    @commands.command(name="cards_random", aliases=["rand"])
    async def _cards_random(ctx, *, black_card=''):
        if black_card == '':
            black_card = database_utils.fetch_cards("black", 1)[0][1]
        num_white_cards = black_card.count("_")
        white_cards = database_utils.fetch_cards("white", num_white_cards)
        #print(white_cards)
        for g in range(num_white_cards):
            black_card = black_card.replace('_', '**'+white_cards[g][1]+'**', 1)
        if not num_white_cards:
            black_card += ' **'+database_utils.fetch_cards("white", 1)[0][1]+"**."
        card_embed = discord.Embed(title="Random CAH combo:", description=black_card)
        card_embed = general_utils.format_embed(ctx.author, card_embed)
        card_embed.colour = discord.Colour.random()
        await ctx.send(embed=card_embed)

        #e,n='E'*5,'\n'
        #await ctx.send(embed=discord.Embed(title=((e*3+n)*2+(e+n)*2)*2+(e*3+n)*2,colour=general_utils.Colours.main))

    Bot.add_command(_cards_random)