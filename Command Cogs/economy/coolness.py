from utils import database_utils, general_utils
from discord.ext import commands
import discord

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
        level = general_utils.exp_to_level(database_utils.fetch_coolness(user_id)[0])
        print(int((level%1)*100-1))
        print(level)
        embed_title = f"{ctx.guild.get_member(user_id).display_name} is coolness level {int(level)}{'!   :sunglasses' if int(level) >= 0 else '.   :confused'}:"
        embed_description = f"`{str(int(level)).rjust(2, ' ')} |{'='*int((level%1)*10-1)}{'>' if int((level%1)*10) > 0 else ''}{' '*int(10-(level%1)*10)}| {str(int(level+1)).rjust(2, ' ')}`"
        level_embed = general_utils.format_embed(ctx.author, discord.Embed(title=embed_title, description=embed_description))
        await ctx.send(embed=level_embed)
    
    Bot.add_command(_coolness)

