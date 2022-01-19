import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cah_info":{
        "aliases":["cah_info"],
        "syntax":"",
        "usage":"Gives info about the cards-against-humanities/helperboi system and how to use it.",
        "category":"cah"
    }})
    @commands.command(name="cah_info")
    async def _cah_info(ctx):
        info_string = """Cards-against-humanity (cah) is a card game similar to "what do you meme", in that you get a card containing a phrase missing key words, and you fill in those blanks with other words/phrases to make the funniest combination possible.
The bot lets you combine black cards (to be filled phrases), with white cards just at random, as well as letting you start and play full cah games.

cah games work by at the start of each round picking a random player to be the czar, whom will act as the judge, and also picking a random black card to be filled.

then, each player (each having 7 random white cards), will pick the white card(s) in their posession they think will be the most hilarious. After everyone has picked, the czar will decide whom had the best combo, the picked player then earns one point, and a new round starts.

Outside of cah games you can also (probably temporarily) submit your own black and white cards to the database to be randomly chosen in cah games and when using `rand`.
Also, some cards or combination of cards might be a bit taboo, but very few should be actually NSFW, though still keep that in mind before using it.
                
Also also, when submitting black cards you only need __one__ underscore (_) to mark one place of insertion for white cards."""

#        An explanation of Cards-against-(humanities/helperboi i still cant decide): (this was taken from [this website] as i cant explain things very concisely.)
#        
#The game's idea is simple- one player reads the question/phrase on a black card, and everyone else fills in the blank with the white card they think is funniest.
#In this its much more simplified; you can submit your own cards and use the `cah_random` command to generate a random combination of white cards and a black card.
#
#The ability to add cards is likely temporary, though once it is inevitably removed because we cannot have nice things, you can try submit cards through the `suggest` command.


        card_embed = discord.Embed(title="CAH Info:", description=info_string)
        card_embed = general_utils.format_embed(ctx.author, card_embed)

        await ctx.send(embed=card_embed)

    Bot.add_command(_cah_info)