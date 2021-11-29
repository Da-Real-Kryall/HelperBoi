import discord, requests, json, random, datetime, django.utils.timezone
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"bored":{
        "aliases":["bored"],
        "syntax":"",
        "usage":"Will give you something to do when you are bored! Powered by (the bored api)[http://www.boredapi.com].\nNote, price is a value between 0 and 1, 0 being free and 1 being quite expensive.",
        "category":"fun"
    }})
    @commands.command(name="bored")
    async def _bored(ctx):
        data = json.loads(requests.get("http://www.boredapi.com/api/activity/").content)
        promptlist = [
            "Here's something you can do!",
            "Try this!",
            "Here is an idea:",
            "How about this?",
            "Why not do this?",
            "This seems fun!",
            "Here is an option:",
            "Have a go at this:"
        ]
        BoredEmbed = discord.Embed(title=random.choice(promptlist))
        BoredEmbed = general_utils.format_embed(ctx.author, BoredEmbed)
        BoredEmbed.add_field(name="Activity:", value=data["activity"], inline=False)
        BoredEmbed.add_field(name="Type:", value=data["type"].capitalize(), inline=True)
        BoredEmbed.add_field(name="Num Participants:", value=data["participants"], inline=True)
        BoredEmbed.add_field(name="Price:", value=data["price"], inline=True)
        BoredEmbed.add_field(name="Accessibility:", value=data["accessibility"], inline=True)
        if data["link"] != '':
            BoredEmbed.add_field(name="Link:", value=data["link"], inline=True)

        await ctx.send(embed=BoredEmbed)

    Bot.add_command(_bored)
