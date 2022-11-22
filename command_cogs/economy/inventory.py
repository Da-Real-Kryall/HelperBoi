import discord, json
from discord.ext import commands
from discord import app_commands
from utils import general_utils, database_utils


class Inventory(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot
        self.item_data = json.load(open("Resources/json/items.json", "r"))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Inventory Cog Loaded")

    @app_commands.command(name="inventory", description="Shows your inventory or the inventory of a specified user.")
    async def _inventory(self, interaction: discord.Interaction, user: discord.User = None):
        if user == None:
            user = interaction.user
        items = database_utils.fetch_user_data(user.id, "inventory")
        if database_utils.fetch_user_data(user.id, "settings")["economy_invisibility"] == True and user != interaction.user:
            await interaction.response.send_message(embed=general_utils.error_embed(interaction.user, message="This user has hidden their economy data...", apologise=True), ephemeral=True)
            return
        embed = general_utils.Embed(author=interaction.user, title=f"{str(user)+''''s''' if user != interaction.user else 'Your'} inventory:")
        description = ""
        x = 0
        for name, amount in items.items():
            if amount != 0:
                x += 1
                description += f"{self.item_data[name]['emoji']}x**{amount}** \u200b \u200b "
                if x == 6:
                    description += "\n"
                    x = 0
        
        embed.description = description[:-5]

        await interaction.response.send_message(embed=embed)

async def setup(Bot):
    await Bot.add_cog(Inventory(Bot))