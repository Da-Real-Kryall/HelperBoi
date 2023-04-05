import json, os, discord
from datetime import datetime
from discord.ext import commands
from utils import general_utils
from discord import app_commands

class PastafarianHoliday(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pastafarian holiday cog loaded.")

    @app_commands.command(name="pastafarian_holiday", description="Returns the current pastafarian holy day.")
    async def _pastafarian_holiday(self, interaction: discord.Interaction) -> None:
        with open(os.getcwd()+"/Resources/json/pastafarian_holidays.json") as file:
            data = json.loads(file.read())
        pf_embed = general_utils.Embed(interaction.user, title=f"Today is {data[datetime.now().strftime('%b %-d')]}!")
        pf_embed.colour = discord.Colour.random()
        await interaction.response.send_message(embed=pf_embed, ephemeral=general_utils.is_ghost(interaction.user.id))
        
async def setup(Bot):
    await Bot.add_cog(PastafarianHoliday(Bot))