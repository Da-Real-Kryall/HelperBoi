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
    async def _impersonate(ctx, user, *, content=''):
        await ctx.message.delete()
        user_id = await general_utils.get_user_id(Bot, ctx, user, True, True)
        if user_id == None:
            return
        user = ctx.guild.get_member(user_id)
        if user == None:
            user = await Bot.fetch_user(user_id)
            username = user.name
        else:
            username = user.display_name
        
        if content == '':
            content = None
            
        files = []
        for attachment in ctx.message.attachments:
            file = await attachment.to_file()
            files += [file]
        
        embeds = []
        for embed in ctx.message.embeds:
            embeds += [embed]

        await general_utils.send_via_webhook(ctx.channel, Bot, message=content, username=username, avatar_url=user.avatar_url, files=files, embeds=embeds)

    Bot.add_command(_impersonate)