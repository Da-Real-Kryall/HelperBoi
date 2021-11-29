import json, os, discord, random
from utils import general_utils
from datetime import datetime
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"brocode":{
        "aliases":["brocode"],
        "syntax":"[number]",
        "usage":"Returns the <number>th (or a random one if no number was given) rule of the Bro-Code.Fair warning; some of these can be a bit nsfw.",
        "category":"fun"
    }})
    @commands.command(name="brocode")
    async def _brocode(ctx, number=''):

        if not general_utils.represents_int(number) and number != '':
            await ctx.send(embed=general_utils.error_embed(False, "Please give a valid number between 1 and 22, or leave blank for a random number."))
            return

        if number == '':
            number = str(random.randint(1,22))

        if int(number) < 1 or int(number) > 22:
            await ctx.send(embed=general_utils.error_embed(False, "Please give a valid number between 1 and 22, or leave blank for a random number."))
            return

        with open(os.getcwd()+"/Recources/json/brocode_rules.json") as file:
            data = json.loads(file.read())

        embed = discord.Embed(title=f"The {general_utils.ordinal(int(number))} rule of the brocode is:", description=data[number])
        await ctx.send(embed=general_utils.format_embed(ctx.author, embed))

    Bot.add_command(_brocode)
