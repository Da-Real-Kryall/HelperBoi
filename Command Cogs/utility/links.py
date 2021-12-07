import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"links":{
        "aliases":["links"],
        "syntax":"",
        "usage":"Returns various web hyperlinks concerning the bot.",
        "category":"utility"
    }})
    @commands.command(name="links")
    async def _links(ctx):
        links = [
            "[Github Repository](https://github.com/Da-Real-Kryall/HelperBoiRewrite)",
            "[Bot Invite](https://discord.com/api/oauth2/authorize?client_id=849543878059098144&permissions=278904302662&scope=bot)"
        ]
        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title="Links:", description="\n".join(links))))
    Bot.add_command(_links)