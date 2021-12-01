import asyncio
from utils import database_utils, general_utils
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"boop":{
        "aliases":["boop"],
        "syntax":"<member>",
        "usage":"Boops the given server member! use the boops command to see how many times someone has been booped, meant as a test for databases.",
        "category":"economy"
    }})
    @commands.guild_only()
    @commands.command(name="boop")
    async def _boop(ctx, *, user=None):
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
            
        database_utils.alter_boops(user_id, 1)

        await ctx.send(f"Booped {ctx.guild.get_member(user_id).display_name}!")
    
    Bot.add_command(_boop)
