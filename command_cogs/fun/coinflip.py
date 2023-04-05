import discord, random
from discord.ext import commands
from utils import general_utils
from discord import app_commands

class Coinflip(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Coinflip cog loaded.")

    @app_commands.command(name="coinflip", description="Flips a coin and tells you the result!")
    async def _coinflip(self, interaction: discord.Interaction) -> None:
        res_dict = {
            "heads":"Heads! :man_bowing:",
            "tails":"Tails! :snake:",
            "edge":"Edge! :o: (This is really rare)"
        }

        if random.randint(1, 6000) == 3000:
            result = "edge"
        else:
            result = list(res_dict)[random.randint(0,1)]

        cf_embed = general_utils.Embed(author=interaction.user, title=res_dict[result])

        await interaction.response.send_message(embed=cf_embed, ephemeral=general_utils.is_ghost(interaction.user.id))

async def setup(Bot):
    await Bot.add_cog(Coinflip(Bot))


#def setup(Bot):
#
#    Bot.command_info.update({"coinflip":{
#        "aliases":["coinflip", "cf"],
#        "syntax":"",
#        "usage":"Flips a coin and tells you the result!",
#        "category":"fun"
#    }})
#    @commands.command(name="coinflip", aliases=['cf'])
#    async def _coinflip(ctx):
#
#        res_dict = {
#            "heads":"Heads! :man_bowing:",
#            "tails":"Tails! :mans_shoe:",
#            "edge":":o It landed on the edge :o:"
#        }
#
#        if random.randint(1, 6000) == 3000:
#            result = "edge"
#        else:
#            result = list(res_dict)[random.randint(0,1)]
#
#        cf_embed = discord.Embed(title=res_dict[result])
#
#        await ctx.send(embed=cf_embed)
#
#    Bot.add_command(_coinflip)
