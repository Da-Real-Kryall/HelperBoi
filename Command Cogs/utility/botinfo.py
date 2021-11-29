import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"botinfo":{
        "aliases":["botinfo"],
        "syntax":"",
        "usage":"Returns info about the bot.",
        "category":"utility"
    }})
    @commands.command(name="botinfo")
    async def _botinfo(ctx):
        InfoEmbed = discord.Embed(title='Bot Info:', description=f'{Bot.user.name} is (evidently) a Discord Bot, made by a highschooler with no life (Kryall#2231) using the Discord.py library, and it\'s purpose is simple yet immensley difficult: **Be Helpful**.\n The bot is meant to be like a cross between Dank-memer and Dyno, except bad... I am planning to keep adding more and more content until I get bored or until it gets verified, which i find unlikely lol.')
        InfoEmbed = general_utils.format_embed(ctx.author, InfoEmbed)
        InfoEmbed.set_thumbnail(url=Bot.user.avatar_url)
        await ctx.send(embed=InfoEmbed)
        
    Bot.add_command(_botinfo)
