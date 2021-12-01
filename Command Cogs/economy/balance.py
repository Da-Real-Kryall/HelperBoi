import discord, asyncio
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
        if user == None:
            user_id = int(ctx.author.id)
        else:
            user_ids = general_utils.get_player_id(Bot, ctx, user)
            if len(user_ids) == 0:
                await ctx.send(embed=general_utils.error_embed(False, "That isnt a member's name!"))
                return
            elif len(user_ids) > 1:
                await ctx.send("Please say the number corresponding to whichever of the possible users you meant:\n"+'\n'.join([f"[{index}] \"{str(ctx.guild.get_member(value))}\"" for index, value in enumerate(list(user_ids.keys()))]))
                
                check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author

                try:
                    msg = await Bot.wait_for('message', timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("nevermind...")
                
                id_list = [value for value in list(user_ids.keys())]

                if general_utils.represents_int(msg.content):
                    if int(msg.content) < len(id_list):
                        user_id = [value for value in list(user_ids.keys())][int(msg.content)]
                    else:
                        await ctx.send(embed=general_utils.error_embed(False, "Please pick a number that was listed."))
                        return
                else:
                    await ctx.send(embed=general_utils.error_embed(False, "Please pick a number that was listed."))
                    return
            else:
                user_id = int(list(user_ids.keys())[0])

        if database_utils.fetch_setting("users", user_id, "economy_invisibility") == True and ctx.author.id != user_id:
            await ctx.send(general_utils.error_embed(True, "This person has activated their economic invisibility; only they can view their balance."))
            return
            
        balance = database_utils.fetch_balance(user_id)

        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"{ctx.guild.get_member(user_id).display_name.capitalize()}'s Balance is §{balance}."), "yellow"))

    Bot.add_command(_balance)