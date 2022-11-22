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

    @app_commands.command(name="balance", description="Shows your balance or the balance of a specified user.")
    async def _balance(self, interaction: discord.Interaction, user: discord.User = None):
        if user == None:
            user = interaction.user
        balance = database_utils.fetch_user_data(user.id, "balance")
        if database_utils.fetch_user_data(user.id, "settings")["economy_invisibility"] == True and user != interaction.user:
            await interaction.response.send_message(embed=general_utils.error_embed(interaction.user, message="This user has hidden their economy data...", apologise=True), ephemeral=True)
            return
        embed = general_utils.Embed(author=interaction.user, title=f"There is **§**{general_utils.si_format(balance)} to your name." if user.id == interaction.user.id else f"{str(user)} has **§**{general_utils.si_format(balance)} to their name.", colour="yellow")
        if balance > 10000:
            embed.set_footer(text=f"{balance}, to be exact.")

        await interaction.response.send_message(embed=embed)

async def setup(Bot):
    await Bot.add_cog(Balance(Bot))