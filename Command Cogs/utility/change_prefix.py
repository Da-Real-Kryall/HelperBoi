import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"change_prefix":{
        "aliases":["change_prefix", "prefix"],
        "syntax":"\`<prefix>\`",
        "usage":"Changes the global bot prefix to the one given in graves, only for the bot owner.",
        "category":"utility"
    }})
    @commands.is_owner()
    @commands.command(name="change_prefix", aliases=["prefix"])
    async def _change_prefix(ctx, *, prefix):

        if prefix[0] != '`' or prefix[-1] != '`':
            await ctx.send(embed=general_utils.error_embed(False, "Please put the new prefix in `graves`"))
            return
        
        old_prefix = str(Bot.command_prefix)

        Bot.command_prefix = prefix[:-1][1:]

        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Changed the prefix from `{old_prefix}` to `{Bot.command_prefix}`.")))
        
    Bot.add_command(_change_prefix)
