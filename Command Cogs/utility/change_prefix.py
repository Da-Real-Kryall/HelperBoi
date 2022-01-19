import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"change_prefix":{
        "aliases":["change_prefix", "ch_pfx"],
        "syntax":"\`<prefix>\`",
        "usage":"Changes the bot prefix in the current guild to the one given in graves, only for the bot owner.",
        "category":"utility"
    }})
    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="change_prefix", aliases=["ch_pfx"])
    async def _change_prefix(ctx, *, prefix):

        if prefix[0] != '`' or prefix[-1] != '`':
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Please put the new prefix in `graves`"))
            return
        
        old_prefix = str(Bot.get_prefix(ctx))

        database_utils.alter_prefix([ctx.guild.id], "update", prefix[1:-1])
        Bot.prefix_cache[ctx.guild.id] = prefix[1:-1]

        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"My prefix in this server has been changed from `{old_prefix}` to `{Bot.get_prefix(ctx)}`.")))
        
    Bot.add_command(_change_prefix)
