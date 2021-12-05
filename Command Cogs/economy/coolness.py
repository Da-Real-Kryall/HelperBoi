from utils import database_utils, general_utils
from discord.ext import commands

def setup(Bot):
    Bot.command_info.update({"coolness":{
        "aliases":["coolness", "level"],
        "syntax":"<member>",
        "usage":"Shows what coolness level a server member is, if no member is given it will show yours.",
        "category":"economy"
    }})
    @commands.guild_only()
    @commands.command(name="coolness", aliases=["level"])
    async def _coolness(ctx, *, user=None):
        user_id = await general_utils.get_user_id(Bot, ctx, user, False)
        if user_id == None:
            return

        await ctx.send(f"{ctx.guild.get_member(user_id).display_name}'s coolness is level {database_utils.fetch_coolness(user_id)[1]}! :sunglasses:")
    
    Bot.add_command(_coolness)

