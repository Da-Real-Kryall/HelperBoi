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
        PrivacyEmbed = discord.Embed(title='My Respection Of Your Privacy:', description='I do not by any means intentionally save/log messages sent, although i will on the other hand log some command usage, this is so i can more easily track the errors and make the bot better faster!')
        PrivacyEmbed.set_thumbnail(url=Bot.user.avatar_url)
        PrivacyEmbed = general_utils.format_embed(ctx.author, PrivacyEmbed)

        await ctx.send(embed=PrivacyEmbed)
        
    Bot.add_command(_privacy)
