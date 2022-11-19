import discord
from discord.ext import commands
from discord import app_commands
from utils import general_utils

class Impersonate(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Impersonate cog loaded.")
        
    @app_commands.command(name="impersonate", description="Fabricates a message to look like it was sent by the given user.")
    async def _impersonate(self, interaction: discord.Interaction, user: discord.User, *, text: str) -> None:
        await general_utils.send_via_webhook(interaction.channel, self.Bot, message=text, username=user.display_name, avatar_url=user.avatar.url)
        await interaction.response.send_message("Message sent!", ephemeral=True, delete_after=5)

async def setup(Bot):
    await Bot.add_cog(Impersonate(Bot))