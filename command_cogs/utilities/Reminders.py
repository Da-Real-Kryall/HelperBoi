import discord, time
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils

class Reminders(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @app_commands.command(name="remind", description="Reminds you of something at a given time.")
    async def _remind(self, interaction: discord.Interaction, message: str, sec: app_commands.Range[int, 1, 59]=0, min: app_commands.Range[int, 1, 59]=0, hour: app_commands.Range[int, 1, 23]=0, day: app_commands.Range[int, 1, 31]=0, month: app_commands.Range[int, 1, 12]=0, year: app_commands.Range[int, 2021, 9999]=0):
        seconds = int(time.time()) + sec + min*60 + hour*3600 + day*86400 + month*2592000 + year*31536000
        id = database_utils.add_reminder(interaction.user.id, seconds, message, interaction.channel.id)
        embed = general_utils.Embed(author=interaction.user, title="Reminder set!", description=f"Your reminder has been set to go off {f'<t:{seconds}:R>.' if seconds != 0 else 'immediately.'}")
        await interaction.response.send_message(embed=embed)
        # start reminder thread if it occurs in the next hour
        if seconds - time.time() < 3600:
            self.Bot.loop.create_task(self.Bot.thread_function(self.Bot, ("reminder", seconds, (id, interaction.user.id, message, seconds, interaction.channel.id))))
            #self.Bot.event_cache.append(("reminder", seconds, (None, interaction.user.id, message, seconds, interaction.channel.id)))
        elif seconds - time.time() < 86400:
            self.Bot.event_cache.append(("reminder", seconds, (id, interaction.user.id, message, seconds, interaction.channel.id)))
async def setup(Bot):
    await Bot.add_cog(Reminders(Bot))