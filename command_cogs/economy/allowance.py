import discord, os, json, random
from discord.ext import commands
from discord import app_commands
from utils import general_utils, database_utils

# A command that can be used once per day; gives an amount of money that scales with the user's coolness level.

class Allowance(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Allowance Cog Loaded")

    @app_commands.command(name="allowance", description="Asks your parents for your daily allowance.")
    async def _allowance(self, interaction: discord.Interaction): #72000
        with open(os.getcwd()+"/Resources/json/command_cooldowns.json") as file:
            cooldowns_json = json.loads(file.read())

        timedelta = database_utils.check_cooldown(interaction.user.id, "allowance", True)

        if timedelta < cooldowns_json["allowance"]:
            res_title = random.choice(["Your parents say no.", "You have already had your daily allowance!", "You have already collected your daily simoleans."])
            hours = (cooldowns_json["allowance"]-timedelta)/60/60
            res_desc = f"Try waiting {'less than an' if hours < 1 else ('about '+('an' if int(hours) == 1 else str(int(hours))))} hour{'s' if int(hours) > 1 else ''}."
        else:
            pay_amount = 1500+(100*database_utils.fetch_user_data(interaction.user.id, "coolness"))
            res_title = random.choice(["Your parents hand you your daily allowance.", "You are handed your allowance.", "You get your daily allowance of simoleans."])
            res_desc = f"+{pay_amount} <:Simolean:769845739043684353> Simoleon{'s' if pay_amount != 1 else ''}"

            database_utils.set_user_data(
                interaction.user.id, 
                "balance",
                pay_amount+database_utils.fetch_user_data(interaction.user.id, "balance")
            )

        embed = general_utils.Embed(author=interaction.user, description=res_desc, title=res_title, colour="yellow")
        await interaction.response.send_message(embed=embed, ephemeral=general_utils.is_ghost(interaction.user.id))

async def setup(Bot):
    await Bot.add_cog(Allowance(Bot))