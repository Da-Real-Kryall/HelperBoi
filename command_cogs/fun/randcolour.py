import discord, random, colorsys
from discord.ext import commands # heh square
from discord import app_commands
from utils import  general_utils

def generate_embeds(mode: str, format: str, amount: int):
    if mode == "normal":
        colours = [discord.Colour.from_rgb(int(random.random()*255), int(random.random()*255), int(random.random()*255)) for g in range(amount)]
    elif mode == "greyscale":
        colours = [discord.Colour.from_hsv(1, 0, random.random()) for g in range(amount)]
    elif mode == "vibrant":
        colours = [discord.Colour.from_hsv(random.random(), 1, 1) for g in range(amount)]

    if format == "hex":
        embeds = [discord.Embed(title=f"#{colour.value:06X}", colour=colour) for colour in colours]
    elif format == "rgb":
        embeds = [discord.Embed(title=f"RGB({colour.r}, {colour.g}, {colour.b})", colour=colour) for colour in colours]
    elif format == "hsv":
        embeds = [discord.Embed(title=f"HSV({', '.join([str(round(x, 3)) for x in colorsys.rgb_to_hsv(float(colour.r)/255, float(colour.g)/255, float(colour.b)/255)])})", colour=colour) for colour in colours]
    
    return embeds

class Controller(discord.ui.View):
    def __init__(self, mode, format, amount):
        super().__init__()
        self.add_item(discord.ui.Button(label=f"Reroll", custom_id=f"rc.{mode}.{format}.{amount}", style=discord.ButtonStyle.blurple))

class RandColour(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("RandColour cog loaded.")

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if "custom_id" in interaction.data:
            data = interaction.data["custom_id"].split(".")
            if data[0] == "rc":
                mode = data[1]
                format = data[2]
                amount = int(data[3])
                embeds = generate_embeds(mode, format, amount)
                await interaction.response.edit_message(embeds=embeds, view=Controller(mode, format, amount))


    @app_commands.command(name="randcolour", description="Returns randomised colour(s) based on the args given.")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="Normal", value="normal"),
            app_commands.Choice(name="Greyscale", value="greyscale"),
            app_commands.Choice(name="Vibrant", value="vibrant"),
        ],
        format=[
            app_commands.Choice(name="Hexadecimal", value="hex"),
            app_commands.Choice(name="RGB", value="rgb"),
            app_commands.Choice(name="HSV", value="hsv"),
        ],
    )
    async def _randcolour(self, interaction: discord.Interaction, mode: str="normal", format: str="hex", amount: app_commands.Range[int, 1, 10]=1) -> None:
        embeds = generate_embeds(mode, format, amount)
        await interaction.response.send_message(embeds=embeds, view=Controller(mode, format, amount), ephemeral=general_utils.is_ghost(interaction.user.id))

    
async def setup(Bot):
    await Bot.add_cog(RandColour(Bot))
