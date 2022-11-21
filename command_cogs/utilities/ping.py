import discord, time
from discord import app_commands
from discord.ext import commands
from utils import general_utils

class Ping(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping cog loaded.")

    @app_commands.command(name="ping", description="Returns the bot latency.")
    async def _ping(self, interaction: discord.Interaction):
        embed1 = general_utils.Embed(author=interaction.user, title="Pinging...", description="You should only see this message for a moment.", colour="yellow")

        e = await interaction.response.send_message(embed=embed1, ephemeral=True)

        before = time.monotonic()

        ping = round((time.monotonic()-before)*1000,1)
        embed2 = general_utils.Embed(
            author=interaction.user,
            title=":ping_pong: Pong and all that.",
            description=f"Latency: {ping}ms\nAPI Latency: {round(self.Bot.latency * 1000, 1)}ms",
            colour="green"
        )

        await interaction.edit_original_response(embed=embed2)

async def setup(Bot):
    await Bot.add_cog(Ping(Bot))
