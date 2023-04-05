import discord
from discord.ext import commands
from discord import app_commands
from utils import general_utils, database_utils

class Coolness(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Coolness Cog Loaded")

    @app_commands.command(name="coolness", description="Shows yours or the given user's level of coolness.")
    async def _coolness(self, interaction: discord.Interaction, user: discord.User = None):
        if user == None:
            user = interaction.user
        coolness = database_utils.fetch_user_data(user.id, "coolness")
        if database_utils.fetch_user_data(user.id, "settings")["economy_invisibility"] == True and user != interaction.user:
            await interaction.response.send_message(embed=general_utils.error_embed(interaction.user, message="This user has hidden their economy data...", apologise=True), ephemeral=True)
            return
        level = general_utils.exp_to_level(coolness)
        embed_title = f"{str(user)} is coolness level {int(level)}{'!   :sunglasses' if int(level) >= 0 else '.   :nerd'}:"
        embed_description = f"`{str(int(level)).rjust(2, ' ')} |{'='*int((level%1)*30-1)}{'>' if int((level%1)*30) > 0 else ''}{' '*int(30-(level%1)*30)}| {str(int(level+1)).rjust(2, ' ')}`"
        embed = general_utils.Embed(author=interaction.user, title=embed_title, description=embed_description, colour="indigo")

        await interaction.response.send_message(embed=embed, ephemeral=general_utils.is_ghost(interaction.user.id))

async def setup(Bot):
    await Bot.add_cog(Coolness(Bot))