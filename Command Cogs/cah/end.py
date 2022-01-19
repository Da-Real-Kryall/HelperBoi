import discord, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"end":{
        "aliases":["end"],
        "syntax":"",
        "usage":"Only usable if you are the game owner, ends the current cah game and tells everyone playing the winner(s).",
        "category":"cah"
    }})
    @commands.command(name="end")
    async def _end(ctx):
        try:
            key = await Bot.cah.stop_cah_game(ctx.author.id)
        except Bot.cah.errors.NotInAGame:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"You arent in a game yet!"))
            return
        except Bot.cah.errors.NotGameOwner:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"You arent the owner of your current game, you need to be the owner to use this command."))
            return

        end_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Ended game `{key}`, hope you enjoyed playing!"), "red")
        await ctx.send(embed=end_embed)
        
    Bot.add_command(_end)