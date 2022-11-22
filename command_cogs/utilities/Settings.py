import discord, os, json, random
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils

with open(os.getcwd()+"/Resources/json/settings_key.json") as file:
    settings_json = json.loads(file.read())


class Controller(discord.ui.View):
    def __init__(self, scroll_index, type):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Toggle", style=discord.ButtonStyle.primary, custom_id=f"{type}.toggle.{scroll_index}"))
        self.add_item(discord.ui.Button(label="Up", style=discord.ButtonStyle.secondary, custom_id=f"{type}.up"))
        self.add_item(discord.ui.Button(label="Down", style=discord.ButtonStyle.secondary, custom_id=f"{type}.down"))
    
    # on_error event
    async def on_error(self, error, item, interaction):
        await interaction.response.send_message(embed=general_utils.error_embed(message=f"The following error occurred while your interaction:\n```py\n{error}\n```"), ephemeral=True)

class Settings(commands.GroupCog, name="settings"):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot


    async def toggle(self, interaction: discord.Interaction):
        #scroll index is the number at the end of the custom id of the first button
        data = interaction.message.components[0].children[0].custom_id.split(".")
        scroll_index = int(data[-1])
        if data[0] == "gs":
            settings = database_utils.fetch_guild_settings(interaction.guild.id)
        elif data[0] == "us":
            settings = database_utils.fetch_user_data(interaction.user.id, "settings")

        embed = interaction.message.embeds[0]

        setting = list(settings.items())[scroll_index][0]
        current_value = settings[setting]

        if data[0] == "gs":
            database_utils.set_guild_settings(interaction.guild.id,  {setting: 1 if current_value == 0 else 0})
        elif data[0] == "us":
            database_utils.set_user_data(interaction.user.id, "settings", {setting: 1 if current_value == 0 else 0})
        
        settings[setting] = 0 if current_value == 1 else 1

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

        embed.description = description

        embed.clear_fields()
        embed.add_field(name="Option Effect:", value=settings_json[{"gs":"servers", "us": "users"}[data[0]]][list(settings.items())[scroll_index][0]]["description"])
        
        await interaction.response.edit_message(embed=embed, view=Controller(scroll_index, data[0]))

    async def scroll_up(self, interaction: discord.Interaction):

        data = interaction.message.components[0].children[0].custom_id.split(".")
        scroll_index = int(data[-1])
        if data[0] == "gs":
            settings = database_utils.fetch_guild_settings(interaction.guild.id)
        elif data[0] == "us":
            settings = database_utils.fetch_user_data(interaction.user.id, "settings")

        embed = interaction.message.embeds[0]

        if scroll_index > 0:
            scroll_index -= 1

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

        embed.description = description

        embed.clear_fields()
        embed.add_field(name="Option Effect:", value=settings_json[{"gs":"servers", "us": "users"}[data[0]]][list(settings.items())[scroll_index][0]]["description"])

        await interaction.response.edit_message(embed=embed, view=Controller(scroll_index, data[0]))

    async def scroll_down(self, interaction: discord.Interaction):
        data = interaction.message.components[0].children[0].custom_id.split(".")
        scroll_index = int(data[-1])
        if data[0] == "gs":
            settings = database_utils.fetch_guild_settings(interaction.guild.id)
        elif data[0] == "us":
            settings = database_utils.fetch_user_data(interaction.user.id, "settings")

        embed = interaction.message.embeds[0]

        if scroll_index < len(settings)-1:
            scroll_index += 1

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

        embed.description = description

        embed.clear_fields()
        embed.add_field(name="Option Effect:", value=settings_json[{"gs":"servers", "us": "users"}[data[0]]][list(settings.items())[scroll_index][0]]["description"])

        await interaction.response.edit_message(embed=embed, view=Controller(scroll_index, data[0]))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings Cog Loaded")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            info = interaction.data["custom_id"].split(".")
            if info[0] in ["gs", "us"]: 
                if info[1] == "toggle":
                    await self.toggle(interaction)
                if info[1] == "up":
                    await self.scroll_up(interaction)
                elif info[1] == "down":
                    await self.scroll_down(interaction)
    

    @app_commands.command(name="personal", description="Will open a GUI for editing personal settings.")
    async def _personal(self, interaction: discord.Interaction) -> None:
        embed = general_utils.Embed(title=f"{interaction.user.display_name}'s Personal Preferences:")

        settings = database_utils.fetch_user_data(interaction.user.id, "settings")

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == 0 else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
        
        embed.description = description

        embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[0][0]]["description"])

        #class Controllerr(discord.ui.View):
        #    def __init__(self, embed: discord.Embed, settings: dict):
        #        super().__init__(timeout=None)
#
        #        self.embed = embed
        #        self.settings = settings
        #        self.scroll_index = 0
#
        #    @discord.ui.button(label="Toggle", style=discord.ButtonStyle.primary)
        #    async def on_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        #        setting = list(self.settings.items())[self.scroll_index][0]
        #        current_value = self.settings[setting]
        #
        #        database_utils.set_user_data(interaction.user.id, "settings", {setting: 1 if current_value == 0 else 0})
        #
        #        self.settings[setting] = 0 if current_value == 1 else 1
        #
        #        description = ""
        #        for index, (setting, value) in enumerate(self.settings.items()):
        #            description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
        #
        #        self.embed.description = description
        #
        #        self.embed.clear_fields()
        #        self.embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[self.scroll_index][0]]["description"])
        #
        #        await interaction.response.edit_message(embed=self.embed, view=self)
#
        #    @discord.ui.button(label="Up", style=discord.ButtonStyle.secondary)
        #    async def on_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        #        if self.scroll_index > 0:
        #            self.scroll_index -= 1
#
        #        description = ""
        #        for index, (setting, value) in enumerate(self.settings.items()):
        #            description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
#
        #        self.embed.description = description
#
        #        self.embed.clear_fields()
        #        self.embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[self.scroll_index][0]]["description"])
        #        
        #        await interaction.response.edit_message(embed=self.embed, view=self)
#
        #    @discord.ui.button(label="Down", style=discord.ButtonStyle.secondary)
        #    async def on_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        #        if self.scroll_index < len(self.settings)-1:
        #            self.scroll_index += 1
#
        #        description = ""
        #        for index, (setting, value) in enumerate(self.settings.items()):
        #            description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
#
        #        self.embed.description = description
#
        #        self.embed.clear_fields()
        #        self.embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[self.scroll_index][0]]["description"])
#
        #        await interaction.response.edit_message(embed=self.embed, view=self)
        scroll_index = 0

        await interaction.response.send_message(embed=embed, view=Controller(scroll_index, "us"), ephemeral=True)

        
    @app_commands.command(name="server", description="Change this server's settings.")
    @app_commands.checks.has_permissions(administrator=True)
    async def _server(self, interaction: discord.Interaction) -> None:
        embed = general_utils.Embed(title=f"Settings for {interaction.guild.name}:")

        settings = database_utils.fetch_guild_settings(interaction.guild.id)

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == 0 else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
        
        embed.description = description

        embed.add_field(name="Option Effect:", value=settings_json["servers"][list(settings.items())[0][0]]["description"])

        scroll_index = 0

        await interaction.response.send_message(embed=embed, view=Controller(scroll_index, "gs"), ephemeral=True)


async def setup(Bot):
    await Bot.add_cog(Settings(Bot))
