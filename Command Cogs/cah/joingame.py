import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"joingame":{
        "aliases":["joingame"],
        "syntax":"<game key>",
        "usage":"Joins the author to the active Cards-Against-Humanity game with the given game key.",
        "category":"cah"
    }})
    @commands.command(name="joingame")
    async def _joingame(ctx, key):
        key = key.upper()
        try:
            await Bot.cah.join_cah_game(ctx.author.id, key)
        except Bot.cah.errors.AlreadyInGame:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"You are already in a game! use the `leavegame` command to leave your curent game."))
            return
        except Bot.cah.errors.NotValidKey:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, f"That doesnt seem to be a valid key/key corresponding to a currently active cah game."))
            return
        except Bot.cah.errors.PlayerNotMessagable:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, f"You appear to have disabled messages from {Bot.user.name}, please enable them before joining."))
            return

            
        joined_embed = general_utils.format_embed(ctx.author, discord.Embed(title="You have joined a game!"), "charcoal")
        
        if isinstance(ctx.channel, discord.channel.DMChannel) == False:
            joined_embed.description = f"Go to your DM with the bot, as that is where the game is played."
        
        await ctx.send(embed=joined_embed)
    Bot.add_command(_joingame)