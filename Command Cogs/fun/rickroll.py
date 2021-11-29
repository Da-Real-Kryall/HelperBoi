import discord, json
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"rickroll":{
        "aliases":["rickroll"],
        "syntax":"",
        "usage":"Gives a bunch of potential rickroll links.\nIf you know of any working links, please let me know and i will add them!",
        "category":"fun"
    }})
    @commands.command(name="rickroll")
    async def _rickroll(ctx):

        with open("Recources/json/rickrolls.json") as file:
            rickroll_json = json.load(file)

        rickroll_embed = discord.Embed(title="Rickroll links list: (that i know of)")
        rickroll_embed = general_utils.format_embed(ctx.author, rickroll_embed, "red")
        
        rickroll_embed.add_field(inline=False, name="Redirects:", value="\n".join(rickroll_json["redirects"]))
        rickroll_embed.add_field(inline=False, name="Videos:", value="\n".join([f"https://youtu.be/{code}" for code in rickroll_json['youtube']]))

        await ctx.send(embed=rickroll_embed)

    Bot.add_command(_rickroll)
