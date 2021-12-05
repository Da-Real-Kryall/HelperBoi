from utils import database_utils, general_utils
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"boop":{
        "aliases":["boop"],
        "syntax":"<member>",
        "usage":"Boops the given user! use the boops command to see how many times someone has been booped, meant as a test for databases and user parsing.",
        "category":"economy"
    }})

    @commands.command(name="boop")
    async def _boop(ctx, *, user=None):
        user_id = await general_utils.get_user_id(Bot, ctx, user, True)
        if user_id == None:
            return
        database_utils.alter_boops(user_id, 1)
        user = await Bot.fetch_user(user_id)
        await ctx.send(f"Booped {user.name}!")
    
    Bot.add_command(_boop)
