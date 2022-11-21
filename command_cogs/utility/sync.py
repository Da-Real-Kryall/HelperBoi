import discord
from discord import app_commands
from discord.ext import commands
from utils import general_utils

class Sync(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    @general_utils.is_owner()
    async def on_ready(self):
        print("Sync cog loaded.")
    
    @commands.command(name="sync", description="Syncs slash commands.")
    @general_utils.is_owner()
    async def __sync(self, ctx) -> None:
        raise ValueError
        fmt = await self.Bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands locally.")
    
    @app_commands.command(name="sync", description="Syncs slash commands.")
    @general_utils.is_owner()
    @app_commands.guilds(discord.Object(id=747834673685594182))
    async def _sync(self, interaction: discord.Interaction):
        if interaction.user.id != 479963507631194133:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="You are not the owner of this bot.", apologise=False), ephemeral=True)
        fmt = await self.Bot.tree.sync()
        await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=f"Synced {len(fmt)} commands globally.", colour="green"))

async def setup(Bot):
    await Bot.add_cog(Sync(Bot))