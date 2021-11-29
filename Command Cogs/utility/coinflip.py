import discord, random
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"coinflip":{
        "aliases":["coinflip", "cf"],
        "syntax":"",
        "usage":"Flips a coin and tells you the result!",
        "category":"utility"
    }})
    @commands.command(name="coinflip", aliases=['cf'])
    async def _coinflip(ctx):

        res_dict = {
            "heads":"Heads! :man_bowing:",
            "tails":"Tails! :mans_shoe:",
            "edge":":o It landed on the edge :o:"
        }

        if random.randint(1, 6000) == 3000:
            result = "edge"
        else:
            result = list(res_dict)[random.randint(0,1)]

        cf_embed = discord.Embed(title=res_dict[result])

        await ctx.send(embed=cf_embed)

    Bot.add_command(_coinflip)
