import discord, os, random
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"asciilist":{
        "aliases":["asciilist"],
        "syntax":"[char number]",
        "usage":"Gives either a text file containing every valid ascii character, or when given a number its corresponding character.",
        "category":"fun"
    }})
    @commands.command(name="asciilist")
    async def _asciilist(ctx, num=''):
        if num == '':
            await ctx.send(file=discord.File(os.getcwd()+'/Recources/plaintext/every_ascii_character.txt'))
        else:
            if general_utils.represents_int(num):
                await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title="`"+chr(int(num))+"`"), timestamp=False))
            else:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "You need to either leave the args blank or specify an integer."))

    Bot.add_command(_asciilist)
