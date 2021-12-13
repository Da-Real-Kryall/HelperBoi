import discord
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"cooltop":{
        "aliases":["cooltop", "leveltop"],
        "syntax":"[isglobal]",
        "usage":"Shows the leaderboard of the coolest/highest level players in the server, or optionally in all applicable servers if 'global' is given.",
        "category":"economy"
    }})#make command return only if its in a DM and the guild-wide board is requested
    @commands.guild_only()
    @commands.command(name="cooltop", aliases=["leveltop"])
    async def _cooltop(ctx, isglobal=''):
        if isglobal != '':
            await ctx.send("global leaderboard hasnt been implemented yet.. sorey! just leave the 'isglobal' arg blank for now.")
            return
        userlist = []
        for user in ctx.guild.members:
            userlist += [[f"{user.display_name[:24]}{' '*(24-len(user.display_name))}", *database_utils.fetch_coolness(user.id)]] # *detabase...{user.discriminator}
        
        userlist.sort(key = lambda l: l[1])
        userlist = list(reversed(userlist))

        userlist = userlist[:10]
        
        res_desc = []
        for index, member in enumerate(userlist):
            index += 1
            res_desc += [f"{index}.{' '*(4-len(str(index)))}Level {member[2]}{' '*(3-len(str(member[2])))}  {member[0]}"]#{' '*(37-len(member[0]))}

        cooltop_embed = general_utils.format_embed(ctx.author, discord.Embed(title="Coolest Bois!", description="`"+("`\n`".join(res_desc))+"`"), "main")
        await ctx.send(embed=cooltop_embed)

    Bot.add_command(_cooltop)