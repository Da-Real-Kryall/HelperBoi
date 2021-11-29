import asyncio
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
        if user == None:
            user_id = int(ctx.author.id)
        else:
            user_ids = general_utils.get_player_id(False, ctx, user)
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

        await ctx.send(f"{ctx.guild.get_member(user_id).display_name}'s coolness is level {database_utils.fetch_coolness(user_id)[1]}! :sunglasses:")
    
    Bot.add_command(_coolness)

