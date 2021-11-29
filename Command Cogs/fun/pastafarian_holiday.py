import json, os, discord
from datetime import datetime
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"pastafarian_holiday":{
        "aliases":["pastafarian_holiday"],
        "syntax":"",
        "usage":"Returns the current pastafarian holiday. Please note some of these are rather icky/nsfw",
        "category":"fun"
    }})
    @commands.command(name="pastafarian_holiday")
    async def _pastafarian_holiday(ctx):
        with open(os.getcwd()+"/Recources/json/pastafarian_holidays.json") as file:
            data = json.loads(file.read())
        pf_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Today is {data[datetime.now().strftime('%b %-d')]}"))
        await ctx.send(embed=pf_embed)
        
    Bot.add_command(_pastafarian_holiday)
