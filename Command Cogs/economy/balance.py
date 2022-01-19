import discord
from utils import database_utils, general_utils
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"balance":{
        "aliases":["balance", "bal"],
        "syntax":"[user]",
        "usage":"Returns the current balance in <:Simolean:769845739043684353> Simoleons of the author, or the user if given.",
        "category":"economy"
    }})
    @commands.command(name="balance", aliases=["bal"])
    async def _balance(ctx, *, user=None):
        user_id = await general_utils.get_user_id(Bot, ctx, user, False)
        if user_id == None:
            return

        if database_utils.fetch_setting("users", user_id, "economy_invisibility") == True and ctx.author.id != user_id:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
            return
        user = await Bot.fetch_user(user_id)
        if user.bot:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
            return

        balance = database_utils.fetch_balance(user_id)

        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"{ctx.guild.get_member(user_id).display_name.capitalize()}'s Balance is §{balance}."), "yellow"))

    Bot.add_command(_balance)