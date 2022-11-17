import discord, os, json, random
from discord.ext import commands
from discord import app_commands
from utils import general_utils

async def setup(Bot):
    with open(os.getcwd()+"/Resources/json/weeb_gif_ids.json") as file:
        gif_json = json.loads(file.read())

    class Emotes(commands.GroupCog, name="emotes"):
        def __init__(self, Bot: commands.Bot):
            self.Bot = Bot
            super().__init__()

        @commands.Cog.listener()
        async def on_ready(self):
            print("Emotes cog loaded.")

        @app_commands.command(name="cuddle", description="Use to give someone a cuddle! (powered by weeb.sh)")
        async def _cuddle(self, interaction: discord.Interaction, user: discord.Member) -> None:

            embed_title = random.choice(["cuddled %s", "you cuddle %s", "you give %s a cuddle"]) % user.display_name
            if random.randint(1,3) != 1:
                embed_title = embed_title.capitalize()
                
            embed_title += random.choice(['.', '!', '...', ''])

            cuddle_embed = general_utils.Embed(author=interaction.user, title=embed_title)
            cuddle_embed.colour = discord.Colour.random()
            cuddle_embed.set_image(url=f"https://cdn.weeb.sh/images/{random.choice(gif_json['cuddle'])}")

            await interaction.response.send_message(embed=cuddle_embed)

        @app_commands.command(name="pat", description="Use to headpat someone! (powered by weeb.sh)")
        async def _pat(self, interaction: discord.Interaction, user: discord.Member) -> None:

            embed_title = random.choice(["patted %s", "you pat %s", "you give %s a head pat", "you give %s a pat on the head"]) % user.display_name
            if random.randint(1,3) != 1:
                embed_title = embed_title.capitalize()

            embed_title += random.choice(['.', '!', '...', ''])

            pat_embed = general_utils.Embed(author=interaction.user, title=embed_title)
            pat_embed.colour = discord.Colour.random()
            pat_embed.set_image(url=f"https://cdn.weeb.sh/images/{random.choice(gif_json['pat'])}")

            await interaction.response.send_message(embed=pat_embed)

        @app_commands.command(name="hug", description="Use to hug someone! (powered by weeb.sh)")
        async def _hug(self, interaction: discord.Interaction, user: discord.Member) -> None:

            embed_title = random.choice(["hugged %s", "you hug %s", "you give %s a hug"]) % user.display_name
            if random.randint(1,3) != 1:
                embed_title = embed_title.capitalize()

            embed_title += random.choice(['.', '!', '...', ''])

            hug_embed = general_utils.Embed(author=interaction.user, title=embed_title)
            hug_embed.colour = discord.Colour.random()
            hug_embed.set_image(url=f"https://cdn.weeb.sh/images/{random.choice(gif_json['hug'])}")

            await interaction.response.send_message(embed=hug_embed)

    await Bot.add_cog(Emotes(Bot))