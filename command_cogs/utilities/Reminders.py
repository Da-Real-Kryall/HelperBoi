import discord, time
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils

class Controller(discord.ui.View):
    def __init__(self, scroll_index, max_index):
        super().__init__()

        self.add_item(discord.ui.Button(
            label="⬆",
            row=0,
            style=discord.ButtonStyle.blurple,
            custom_id="reminders.previous",
            disabled=True if scroll_index <= 0 else False
        ))

        self.add_item(discord.ui.Button(
            label="⬇",
            row=1,
            style=discord.ButtonStyle.blurple,
            custom_id="reminders.next",
            disabled=True if scroll_index >= max_index else False
        ))
        
        self.add_item(discord.ui.Button(
            label="💥",
            row=0,
            style=discord.ButtonStyle.red,
            custom_id="reminders.delete",
            disabled=False if max_index > -1 else True
        ))
    
    async def on_error(self, error, item, interaction):
        await interaction.followup.send_message(embed=general_utils.error_embed(message=f"The following error occurred while your interaction:\n```py\n{error}\n```"), ephemeral=True)

async def _next(interaction: discord.Interaction):
    await interaction.response.defer() # [(id, user_id, message, timestamp, channel_id)]
    embed = interaction.message.embeds[0]
    reminders = database_utils.fetch_reminders(interaction.user.id)
    # footer: "Reminder 2 of 4"
    scroll_index = int(embed.footer.text.split(" ")[1]) - 1
    max_index = int(embed.footer.text.split(" ")[3]) - 1
    
    scroll_index += 1

    embed.set_footer(text=f"Reminder {scroll_index + 1} of {max_index + 1}")
    embed.description = ""
    for index, reminder in enumerate(reminders):
        embed.description += f"` {'>' if index == scroll_index else ' '} ` **[**<t:{reminder[3]}:R>**]** - \"{reminder[2]}\"\n"

    view = Controller(scroll_index, max_index)
    await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

async def _previous(interaction: discord.Interaction):
    await interaction.response.defer() # [(id, user_id, message, timestamp, channel_id)]
    embed = interaction.message.embeds[0]
    reminders = database_utils.fetch_reminders(interaction.user.id)
    # footer: "Reminder 2 of 4"
    scroll_index = int(embed.footer.text.split(" ")[1]) - 1
    max_index = int(embed.footer.text.split(" ")[3]) - 1
    
    scroll_index -= 1

    embed.set_footer(text=f"Reminder {scroll_index + 1} of {max_index + 1}")
    embed.description = ""
    for index, reminder in enumerate(reminders):
        embed.description += f"` {'>' if index == scroll_index else ' '} ` **[**<t:{reminder[3]}:R>**]** - \"{reminder[2]}\"\n"

    view = Controller(scroll_index, max_index)
    await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

async def _delete(interaction: discord.Interaction):
    await interaction.response.defer() # [(id, user_id, message, timestamp, channel_id)]
    embed = interaction.message.embeds[0]
    # footer: "Reminder 2 of 4"
    scroll_index = int(embed.footer.text.split(" ")[1]) - 1

    reminders = database_utils.fetch_reminders(interaction.user.id)
    database_utils.remove_reminders([reminders[scroll_index][0]])
    reminders = database_utils.fetch_reminders(interaction.user.id)
    max_index = int(embed.footer.text.split(" ")[3]) - 2

    if scroll_index > max_index:
        scroll_index = max_index

    embed.set_footer(text=f"Reminder {scroll_index + 1} of {max_index}")
    embed.description = ""
    for index, reminder in enumerate(reminders):
        embed.description += f"` {'>' if index == scroll_index else ' '} ` **[**<t:{reminder[3]}:R>**]** - \"{reminder[2]}\"\n"

    view = Controller(scroll_index, max_index)
    await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

class Reminders(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("Reminders cog loaded.")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if "custom_id" in interaction.data:
            if interaction.data["custom_id"].startswith("reminders."):
                if interaction.data["custom_id"].split(".")[1] == "delete":
                    await _delete(interaction)
                elif interaction.data["custom_id"].split(".")[1] == "next":
                    await _next(interaction)
                elif interaction.data["custom_id"].split(".")[1] == "previous":
                    await _previous(interaction)

    @app_commands.command(name="remind", description="Reminds you of something at a given time.")
    async def _remind(self, interaction: discord.Interaction, message: str, seconds: app_commands.Range[int, 1, 59]=0, minutes: app_commands.Range[int, 1, 59]=0, hours: app_commands.Range[int, 1, 23]=0, days: app_commands.Range[int, 1, 31]=0, months: app_commands.Range[int, 1, 12]=0, years: app_commands.Range[int, 2021, 9999]=0):
        seconds = int(time.time()) + seconds + minutes * 60 + hours * 3600 + days * 86400 + months * 2592000 + years * 31536000
        id = database_utils.add_reminder(interaction.user.id, seconds, message, interaction.channel.id)
        embed = general_utils.Embed(author=interaction.user, title="Reminder set!", description=f"Your reminder has been set to go off {f'<t:{seconds}:R>.' if seconds != 0 else 'immediately.'}")
        await interaction.response.send_message(embed=embed)
        if seconds - time.time() < 3600:
            self.Bot.loop.create_task(self.Bot.thread_function(self.Bot, ("reminder", seconds, (id, interaction.user.id, message, seconds, interaction.channel.id))))
        elif seconds - time.time() < 86400:
            self.Bot.event_cache.append(("reminder", seconds, (id, interaction.user.id, message, seconds, interaction.channel.id)))

    @app_commands.command(name="reminders", description="Shows a GUI for managing your reminders.")
    async def _reminders(self, interaction: discord.Interaction):
        await interaction.response.defer()
        reminders = database_utils.fetch_reminders(interaction.user.id)
        if len(reminders) == 0:
            embed = general_utils.Embed(author=interaction.user, title="No reminders!", description="You don't have any reminders set.")
            await interaction.followup.send(embed=embed)
            return
        embed = general_utils.Embed(author=interaction.user, title="Your reminders", description="")
        for index, reminder in enumerate(reminders):
            embed.description += f"` {'>' if index == 0 else ' '} ` **[**<t:{reminder[3]}:R>**]** - \"{reminder[2]}\"\n"
        embed.set_footer(text=f"Reminder 1 of {len(reminders)}")
        view = Controller(0, len(reminders) - 1)
        await interaction.followup.send(embed=embed, view=view)

async def setup(Bot):
    await Bot.add_cog(Reminders(Bot))