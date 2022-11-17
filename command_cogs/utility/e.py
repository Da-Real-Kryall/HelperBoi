import discord
from discord import app_commands
from discord.ext import commands
from utils import general_utils

class E(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("E cog loaded.")
    
    @app_commands.command(name="e", description="Test command. Makes E.")
    async def _e(self, interaction: discord.Interaction) -> None:
        e,n='E'*5,'\n'
        await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=((e*3+n)*2+(e+n)*2)*2+(e*3+n)*2))

async def setup(Bot):
    await Bot.add_cog(E(Bot))