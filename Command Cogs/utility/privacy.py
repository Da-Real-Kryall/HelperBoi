import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"privacy":{
        "aliases":["privacy"],
        "syntax":"",
        "usage":"Returns info regarding the bot's use (or lack of!) of your info.",
        "category":"utility"
    }})
    @commands.command(name="privacy")
    async def _privacy(ctx):
        PrivacyEmbed = discord.Embed(title='My Respection Of Your Privacy:', description='I do not by any means intentionally save/log messages sent, and i do not save the names of users within their economy data; only their user ids, although i will on the other hand sometimes log command usage, this is to more easily track errors and improve the bot faster.')
        PrivacyEmbed.set_thumbnail(url=Bot.user.avatar.url)
        PrivacyEmbed = general_utils.format_embed(ctx.author, PrivacyEmbed)

        await ctx.send(embed=PrivacyEmbed)
        
    Bot.add_command(_privacy)
