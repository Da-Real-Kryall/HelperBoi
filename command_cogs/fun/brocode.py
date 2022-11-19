import json, os, discord, random
from utils import general_utils
from discord.ext import commands
from discord import app_commands

class Brocode(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Brocode cog loaded.")

    @app_commands.command(name="brocode", description="Returns the Nth brocode rule. (slight nsfw warning)")
    async def _brocode(self, interaction: discord.Interaction, number: app_commands.Range[int, 1, 22]=None) -> None:
        if number is None:
            number = random.randint(1, 22)

        with open(os.getcwd()+"/Resources/json/brocode_rules.json") as file:
            data = json.loads(file.read())

        embed = general_utils.Embed(author=interaction.user, title=f"The {general_utils.ordinal(int(number))} rule of the brocode is:", description=data[number])
        embed.colour = discord.Colour.random()
        await interaction.response.send_message(embed=embed)

async def setup(Bot):
    await Bot.add_cog(Brocode(Bot))
