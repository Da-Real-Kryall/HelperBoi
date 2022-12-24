import discord, time, random, time
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils

class Submissions(commands.GroupCog, name="submit"):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Submissions cog loaded.")

    @app_commands.command(name="bug", description="Submits a bugreport to the bot developer.")
    async def _bug(self, interaction: discord.Interaction, content: str):
        await interaction.response.defer()
        embed = general_utils.Embed(author=interaction.user, title="Bugreport submitted!", description="Your bugreport has been submitted to the bot developer.")

        if random.randint(1, 20) == 1:
            embed.set_footer(text=":cookie: You got a cookie! Thanks for helping improve the bot!")
            await database_utils.set_user_data(interaction.user.id, "items", {"biscuit": database_utils.fetch_user_data(interaction.user.id, "items")["biscuit"] + 1})
        
        await interaction.followup.send(embed=embed)

        database_utils.add_submission(interaction.user.id, content, int(time.time()), "bug")

        embed = general_utils.Embed(author=interaction.user, title="Bugreport:", description=content)

        if self.Bot.owner_id == None:
            self.Bot.owner_id = general_utils.bot_owner_id
        user = self.Bot.get(self.Bot.owner_id)
        if user == None:
            user = await self.Bot.fetch_user(self.Bot.owner_id)
        await user.send(embed=embed)

    @app_commands.command(name="suggestion", description="Submits a suggestion to the bot developer.")
    async def _suggestion(self, interaction: discord.Interaction, content: str):
        await interaction.response.defer()
        embed = general_utils.Embed(author=interaction.user, title="Suggestion submitted!", description="Your suggestion has been submitted to the bot developer. Thank you!")

        if random.randint(1, 20) == 1:
            embed.set_footer(text=":cookie: You got a cookie! Thanks for helping improve the bot!")
            await database_utils.set_user_data(interaction.user.id, "items", {"biscuit": database_utils.fetch_user_data(interaction.user.id, "items")["biscuit"] + 1})
        
        await interaction.followup.send(embed=embed)

        database_utils.add_submission(interaction.user.id, content, int(time.time()), "suggestion")

        embed = general_utils.Embed(author=interaction.user, title="Suggestion:", description=content)

        if self.Bot.owner_id == None:
            self.Bot.owner_id = general_utils.bot_owner_id
        user = self.Bot.get(self.Bot.owner_id)
        if user == None:
            user = await self.Bot.fetch_user(self.Bot.owner_id)
        await user.send(embed=embed)


async def setup(Bot):
    await Bot.add_cog(Submissions(Bot))