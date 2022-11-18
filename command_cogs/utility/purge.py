import discord
from discord.ext import commands
from utils import general_utils
from discord import app_commands

class Purge(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Purge cog loaded.")
    
    @app_commands.command(name="purge", description="Deletes X messages from the current channel. Use this sparingly and wisely.")
    @app_commands.default_permissions(manage_messages=True)
    async def _purge(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]) -> None:
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Deleted {amount} messages.", delete_after=10, ephemeral=True)

async def setup(Bot):
    await Bot.add_cog(Purge(Bot))