import discord, os, sys
from discord.ext import commands
from utils import general_utils
from discord import app_commands

class ReloadCog(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Reload cog loaded.")
    
    @app_commands.command(name="reload", description="Reloads a cog.")
    @app_commands.guilds(discord.Object(id=747834673685594182))
    async def _reload(self, interaction: discord.Interaction, cog: str) -> None:
        try:
            self.Bot.reload_extension("command_cogs."+cog)
            await interaction.response.send_message(embed=general_utils.success_embed(message="Cog reloaded successfully."))
        except Exception as e:
            await interaction.response.send_message(embed=general_utils.error_embed(message=f"The following error occurred while reloading the cog:\n```py\n{e}\n```"))
        
async def setup(Bot):
    await Bot.add_cog(ReloadCog(Bot))