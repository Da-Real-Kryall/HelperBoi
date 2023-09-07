import discord, time
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils


def remind_embed_modifier(embed: discord.Embed, scroll_index: int, interaction: discord.Interaction) -> discord.Embed:
    reminders = database_utils.fetch_reminders(interaction.user.id)
    length = int(embed.footer.text.split(" ")[3])
    embed.set_footer(text=f"Reminder {min(scroll_index+1, length)} of {length}")
    embed.clear_fields()
    embed.description = ""
    offset = 0
    if len(reminders) > 10:
        offset = scroll_index - 5
        if offset < 0:
            offset = 0
        if offset > len(reminders) - 10:
            offset = len(reminders) - 10
    if offset != 0:
        embed.description += f"[{offset} more]\n"
        
    for index, reminder in enumerate(reminders[offset:offset+10], offset):
        embed.description += f"` {'>' if index == scroll_index else ' '} ` **[**<t:{reminder[3]}:R>**]** - \"{reminder[2][:16]+('...' if len(reminder[2]) > 16 else '')}\"\n"
        if index == scroll_index:
            embed.add_field(name="Message:", value=reminder[2])
    if offset != len(reminders) - 10:
        embed.description += f"[{len(reminders)-10 - offset} more]"

    return embed

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
                def delete_reminder(scroll_index: int) -> int:
                    reminders = database_utils.fetch_reminders(interaction.user.id)
                    database_utils.remove_reminders([reminders[scroll_index][0]])
                    reminders = database_utils.fetch_reminders(interaction.user.id)
                    return max(scroll_index-1, 0)
                functions = general_utils.make_functions_dict("reminders", remind_embed_modifier, delete_reminder)
                await general_utils.interaction_listener_generator("reminders", functions)(interaction)
                
    @app_commands.command(name="remind", description="Reminds you of something at a given time.")
    async def _remind(self, interaction: discord.Interaction, message: str, seconds: app_commands.Range[int, 1, 59]=0, minutes: app_commands.Range[int, 1, 59]=0, hours: app_commands.Range[int, 1, 23]=0, days: app_commands.Range[int, 1, 31]=0, months: app_commands.Range[int, 1, 12]=0, years: app_commands.Range[int, 2021, 9999]=0):
        seconds = int(time.time()) + seconds + minutes * 60 + hours * 3600 + days * 86400 + months * 2592000 + years * 31536000
        id = database_utils.add_reminder(interaction.user.id, seconds, message, interaction.channel.id)
        embed = general_utils.Embed(author=interaction.user, title="Reminder set!", description=f"Your reminder has been set to go off {f'<t:{seconds}:R>.' if seconds != 0 else 'immediately.'}")
        await interaction.response.send_message(embed=embed, ephemeral=general_utils.is_ghost(interaction.user.id))
        if seconds - time.time() < 3600:
            self.Bot.loop.create_task(self.Bot.thread_function(self.Bot, ("reminder", seconds, (id, interaction.user.id, message, seconds, interaction.channel.id))))
        elif seconds - time.time() < 86400:
            self.Bot.event_cache.append(("reminder", seconds, (id, interaction.user.id, message, seconds, interaction.channel.id)))

    @app_commands.command(name="reminders", description="Shows a GUI for managing your reminders.")
    async def _reminders(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=general_utils.is_ghost(interaction.user.id))
        reminders = database_utils.fetch_reminders(interaction.user.id)
        if len(reminders) == 0:
            embed = general_utils.Embed(author=interaction.user, title="No reminders!", description="You don't have any reminders set.")
            await interaction.followup.send(embed=embed)
            return

        embed = general_utils.Embed(author=interaction.user, title="Your reminders", description="")
        interaction.data.update({"custom_id": "reminders.0"})
        embed.set_footer(text=f"Reminder 1 of {len(reminders)}")
        embed = remind_embed_modifier(embed, 0, interaction)

        await interaction.followup.send(embed=embed, view=general_utils.Controller("reminders", 0, len(reminders)))

async def setup(Bot):
    await Bot.add_cog(Reminders(Bot))