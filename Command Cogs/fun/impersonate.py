import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"impersonate":{
        "aliases":["impersonate", "imp"],
        "syntax":"<user> <text>",
        "usage":"Lets you impersonate the given user by sending a message tat looks like it was sent by said user, containing the your given text content.",
        "category":"fun"
    }})
    @commands.command(name="impersonate", aliases=['imp'])
    async def _impersonate(ctx, user, content):
        user_id = await general_utils.get_user_id(Bot, ctx, user, True, True)
        if user_id == None:
            return
        user = ctx.guild.get_member(user_id)
        if user == None:
            user = await Bot.fetch_user(user_id)
            await general_utils.send_via_webhook(ctx, Bot, content, user.name, user.avatar_url)
        else:
            await general_utils.send_via_webhook(ctx, Bot, content, user.display_name, user.avatar_url)

    Bot.add_command(_impersonate)