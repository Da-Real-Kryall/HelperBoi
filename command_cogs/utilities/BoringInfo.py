import discord
from discord.ext import commands
from discord import app_commands
from utils import general_utils

class BoringInfo(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("BoringInfo Cog Loaded")

    @app_commands.command(name="privacy", description="Returns info regarding the bot's use (or lack of!) of your info.")
    async def _privacy(self, interaction: discord.Interaction) -> None:
        PrivacyEmbed = general_utils.Embed(author=interaction.user, title='My Respection Of Your Privacy:', description="I do not by any means intentionally save/log message content/data, in spite of having the message content intent. If you do not trust my word on this, you can check the bot source.\n\nI also do not save the names of users within economy data; only their ID's.\n\nOne thing I do occasionaly save is command usage and command errors, so that I can more easily hunt down errors and make the bot better faster.\n\nI also, for your peace of mind, deafen myself in all voice channels I join.")

        await interaction.response.send_message(embed=PrivacyEmbed, ephemeral=True)

    @app_commands.command(name="source", description="Returns the bot's source code link.")
    async def _source(self, interaction: discord.Interaction) -> None:
        SourceEmbed = general_utils.Embed(author=interaction.user, title="Helperboi is built using Python & discord.py.", description="It's open source too! You can find the source code here on GitHub:\nhttps://github.com/Da-Real-Kryall/HelperBoi")
        SourceEmbed.set_thumbnail(url=self.Bot.user.avatar.url)

        await interaction.response.send_message(embed=SourceEmbed, ephemeral=True)


async def setup(Bot):
    await Bot.add_cog(BoringInfo(Bot))