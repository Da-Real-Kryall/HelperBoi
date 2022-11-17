import discord, os, asyncio
from discord.ext import commands
from discord import app_commands

Bot = commands.Bot(command_prefix="!kbr ", intents=discord.Intents.all())


#class Pog(commands.Cog):
#    def __init__(self, Bot: commands.Bot):
#        self.Bot = Bot
#
#    @commands.Cog.listener()
#    async def on_ready(self):
#        print("Pog cog loaded.")
#
@Bot.command()
async def sync(ctx) -> None:
    fmt = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(fmt)} commands globally.")
    return

@Bot.tree.command(name="poggers", description="Poggers if this works")
async def poggers(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("pog")


@Bot.event
async def on_connect():
    print("im ready")

with open(os.getcwd()+"/token.txt") as nonofile:
    nonokey = nonofile.read()


Bot.run(nonokey)
