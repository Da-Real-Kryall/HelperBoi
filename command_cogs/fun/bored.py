import requests, json, random, discord
from discord.ext import commands
from utils import general_utils
from discord import app_commands


price_dict = {
    0:"Free",
    0.1:"Cheap",
    0.2:"Cheap",
    0.3:"Cheap",
    0.4:"Cheap",
    0.5:"Moderate",
    0.6:"Moderate",
    0.7:"Moderate",
    0.8:"Expensive",
    0.9:"Expensive",
    1:"Very Expensive"
}
accessibility_dict = {
    0:"Very Accessible",
    0.1:"Accessible",
    0.2:"Accessible",
    0.3:"Accessible",
    0.4:"Moderately Accessible",
    0.5:"Moderately Accessible",
    0.6:"Moderately Accessible",
    0.7:"Hardly Accessible",
    0.8:"Hardly Accessible",
    0.9:"Hardly Accessible",
    1:"Very Inaccessible"
}

def generate_embed(interaction: discord.Interaction) -> discord.Embed:
    data = json.loads(requests.get("http://www.boredapi.com/api/activity/").content)

    BoredEmbed = general_utils.Embed(author=interaction.user, title=data["activity"]+"!")
    
    BoredEmbed.description = f"""{f"**Type:** {data['type']}"}
{f"**Participants:** {data['participants']}" if data['participants'] != 1 else ""}
{f"**Price:** {price_dict[round(data['price'],1)]} ({int(data['price']*100)}/100)"}
{f"**Link:** {data['link']}" if data['link'] != "" else ""}
{f"**Accessibility:** {accessibility_dict[round(data['accessibility'],1)]} ({int(data['accessibility']*100)}/100)"}
""".replace("\n\n", "\n").replace("\n\n", "\n")

    BoredEmbed.colour = discord.Colour.random()
    return BoredEmbed


class Controller(discord.ui.View):
    @discord.ui.button(label="Reroll", style=discord.ButtonStyle.blurple)
    async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=generate_embed(interaction), view=self)


class Bored(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bored cog loaded.")

    @app_commands.command(name="bored", description="Sends a random activity for when you're bored. Powered by (the bored api)[http://www.boredapi.com].")
    async def _bored(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=generate_embed(interaction), view=Controller(), ephemeral=general_utils.is_ghost(interaction.user.id))

async def setup(Bot):
    await Bot.add_cog(Bored(Bot))
