import discord
from discord.ext import commands
from discord import app_commands
from utils import general_utils, database_utils

class Balance(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Balance Cog Loaded")

    @app_commands.command(name="balance", description="Shows your balance.")
    async def _balance(self, interaction: discord.Interaction):
        balance = database_utils.fetch_user_data(interaction.user.id, "balance")
        embed = general_utils.Embed(author=interaction.user, title=f"Your balance is §{general_utils.si_format(balance)}", colour="yellow")
        if balance > 1000:
            embed.set_footer(text="§{balance}, to be exact.")

        await interaction.response.send_message(embed=embed)

async def setup(Bot):
    await Bot.add_cog(Balance(Bot))