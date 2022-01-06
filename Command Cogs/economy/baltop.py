import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"baltop":{
        "aliases":["baltop"],
        "syntax":"[isglobal]",
        "usage":"Shows the leaderboard of the richest players in the server, or optionally in all applicable servers if 'global' is given.",
        "category":"economy"
    }})#make command return only if its in a DM and the guild-wide board is requested
    @commands.guild_only()
    @commands.command(name="baltop")
    async def _baltop(ctx, isglobal=''):
        userlist = []
        if isglobal.lower() == 'global' or ctx.guild == None:
            async with ctx.typing():
                userlist = await Bot.request_global("baltop")
                res_title = "Richest Bois! (global)"
        elif isglobal == '' and ctx.guild != None:
            res_title = "Richest Bois!"
            for user in ctx.guild.members:
                if user.bot == False:
                    if database_utils.fetch_setting("users", user.id, "economy_invisibility") == False:
                        userlist += [[f"{user.display_name[:24]}{' '*(24-len(user.display_name))}", database_utils.fetch_balance(user.id)]] # *detabase...{user.discriminator}
            userlist.sort(key = lambda l: l[1])
            userlist = list(reversed(userlist))
            userlist = userlist[:10]
        else: #invalid isglobal arg, error and return
            await ctx.send(embed=general_utils.error_embed(False, "Please either give 'global' as the isglobal arg OR leave it blank, for the global leaderboard or the serverwide one respectively."))
            return
        res_desc = []
        for index, member in enumerate(userlist):
            index += 1
            res_desc += [f"{index}.{' '*(4-len(str(index)))}§{general_utils.si_suffix(member[1]) if member[1] > 1000 else member[1]}{' '*(7-len(str(general_utils.si_suffix(member[1]) if member[1] > 1000 else member[1])))}  {member[0]}"]#{' '*(37-len(member[0]))}

        baltop_embed = general_utils.format_embed(ctx.author, discord.Embed(title=res_title, description="`"+("`\n`".join(res_desc))+"`"), "yellow")
        await ctx.send(embed=baltop_embed)

    Bot.add_command(_baltop)