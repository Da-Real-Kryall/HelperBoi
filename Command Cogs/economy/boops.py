from utils import database_utils, general_utils
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"boops":{
        "aliases":["boops"],
        "syntax":"<member>",
        "usage":"Returns how many times the given server member has been booped! meant as a test for databases.",
        "category":"economy"
    }})
    @commands.guild_only()
    @commands.command(name="boops")
    async def _boops(ctx, *, user=None):
        user_id = await general_utils.get_user_id(Bot, ctx, user, True)
        if user_id == None:
            return
        user = await Bot.fetch_user(user_id)
        if user.bot:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
            return

        boops = database_utils.fetch_boops(user_id)

        await ctx.send(f"{ctx.guild.get_member(user_id).display_name} has been booped {boops} times!")

    Bot.add_command(_boops)
