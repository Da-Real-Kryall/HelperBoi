import discord, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cah_start":{
        "aliases":["cah_start"],
        "syntax":"",
        "usage":"Starts the Cards-Against-Humanity game that you are owner of, if it is currently on standby to begin and hasnt started already. Used once all your friend(s) have joined and are ready to play.",
        "category":"cah"
    }})
    @commands.command(name="cah_start")
    async def _cah_start(ctx):
        #key = Bot.cah.current_active_players[ctx.author.id]
        #game = Bot.cah.current_cah_sessions[key]
        #if game["owner"] != ctx.author.id:
        #    await ctx.send(f"You arent the owner of this game!")
        #await ctx.send(f"Game started with id {key}")
        try:
            await Bot.cah.run_cah_game(ctx.author.id)
        except Bot.cah.errors.NotInGame:
            await ctx.send(embed=general_utils.error_embed(False, f"You arent in a game yet!"))
            return
        except Bot.cah.errors.NotGameOwner:
            await ctx.send(embed=general_utils.error_embed(False, f"You arent the owner of your current game, you need to be the owner to use this command."))
            return

        start_embed = general_utils.format_embed(ctx.author, discord.Embed(title="The game is now starting, have fun!"), "charcoal")
        
        if isinstance(ctx.channel, discord.channel.DMChannel) == False:
            start_embed.description = f"Go to your DM with the bot, as that is where the game is being played."
        
        await ctx.send(embed=start_embed)
        
    Bot.add_command(_cah_start)