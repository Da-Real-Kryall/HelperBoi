import discord, os, json, random
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils

with open(os.getcwd()+"/Resources/json/settings_key.json") as file:
    settings_json = json.loads(file.read())

class Settings(commands.GroupCog, name="settings"):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings Cog Loaded")

    @app_commands.command(name="personal", description="Will open a GUI for editing personal settings.")
    async def _personal(self, interaction: discord.Interaction) -> None:
        embed = general_utils.Embed(title=f"{interaction.user.display_name}'s Personal Preferences:")

        settings = database_utils.fetch_user_data(interaction.user.id, "settings")

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == 0 else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
        
        embed.description = description

        embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[0][0]]["description"])

        class Controller(discord.ui.View):
            def __init__(self, embed: discord.Embed, settings: dict):
                super().__init__(timeout=None)

                self.embed = embed
                self.settings = settings
                self.scroll_index = 0

            @discord.ui.button(label="Toggle", style=discord.ButtonStyle.primary)
            async def on_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
                setting = list(self.settings.items())[self.scroll_index][0]
                current_value = self.settings[setting]

                database_utils.set_user_data(interaction.user.id, "settings", {setting: 1 if current_value == 0 else 0})

                self.settings[setting] = 0 if current_value == 1 else 1

                description = ""
                for index, (setting, value) in enumerate(self.settings.items()):
                    description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

                self.embed.description = description

                self.embed.clear_fields()
                self.embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[self.scroll_index][0]]["description"])

                await interaction.response.edit_message(embed=self.embed, view=self)

            @discord.ui.button(label="Up", style=discord.ButtonStyle.secondary)
            async def on_up(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.scroll_index > 0:
                    self.scroll_index -= 1

                description = ""
                for index, (setting, value) in enumerate(self.settings.items()):
                    description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

                self.embed.description = description

                self.embed.clear_fields()
                self.embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[self.scroll_index][0]]["description"])
                
                await interaction.response.edit_message(embed=self.embed, view=self)

            @discord.ui.button(label="Down", style=discord.ButtonStyle.secondary)
            async def on_down(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.scroll_index < len(self.settings)-1:
                    self.scroll_index += 1

                description = ""
                for index, (setting, value) in enumerate(self.settings.items()):
                    description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

                self.embed.description = description

                self.embed.clear_fields()
                self.embed.add_field(name="Option Effect:", value=settings_json["users"][list(settings.items())[self.scroll_index][0]]["description"])

                await interaction.response.edit_message(embed=self.embed, view=self)

        await interaction.response.send_message(embed=embed, view=Controller(embed, settings), ephemeral=True)

        
    @app_commands.command(name="server", description="Change this server's settings.")
    @app_commands.default_permissions(administrator=True)
    async def _server(self, interaction: discord.Interaction) -> None:
        embed = general_utils.Embed(title=f"Settings for {interaction.guild.name}:")

        settings = database_utils.fetch_guild_settings(interaction.user.id)

        description = ""
        for index, (setting, value) in enumerate(settings.items()):
            description += f"` {'>' if index == 0 else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"
        
        embed.description = description

        embed.add_field(name="Option Effect:", value=settings_json["servers"][list(settings.items())[0][0]]["description"])

        class Controller(discord.ui.View):
            def __init__(self, embed: discord.Embed, settings: dict):
                super().__init__(timeout=None)

                self.embed = embed
                self.settings = settings
                self.scroll_index = 0

            @discord.ui.button(label="Toggle", style=discord.ButtonStyle.primary)
            async def on_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
                setting = list(self.settings.items())[self.scroll_index][0]
                current_value = self.settings[setting]

                database_utils.set_user_data(interaction.user.id, "settings", {setting: 1 if current_value == 0 else 0})

                self.settings[setting] = 0 if current_value == 1 else 1

                description = ""
                for index, (setting, value) in enumerate(self.settings.items()):
                    description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

                self.embed.description = description

                self.embed.clear_fields()
                self.embed.add_field(name="Option Effect:", value=settings_json["servers"][list(settings.items())[self.scroll_index][0]]["description"])

                await interaction.response.edit_message(embed=self.embed, view=self)

            @discord.ui.button(label="Up", style=discord.ButtonStyle.secondary)
            async def on_up(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.scroll_index > 0:
                    self.scroll_index -= 1

                description = ""
                for index, (setting, value) in enumerate(self.settings.items()):
                    description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

                self.embed.description = description

                self.embed.clear_fields()
                self.embed.add_field(name="Option Effect:", value=settings_json["servers"][list(settings.items())[self.scroll_index][0]]["description"])
                
                await interaction.response.edit_message(embed=self.embed, view=self)

            @discord.ui.button(label="Down", style=discord.ButtonStyle.secondary)
            async def on_down(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.scroll_index < len(self.settings)-1:
                    self.scroll_index += 1

                description = ""
                for index, (setting, value) in enumerate(self.settings.items()):
                    description += f"` {'>' if index == self.scroll_index else ' '} ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`\n"

                self.embed.description = description

                self.embed.clear_fields()
                self.embed.add_field(name="Option Effect:", value=settings_json["servers"][list(settings.items())[self.scroll_index][0]]["description"])

                await interaction.response.edit_message(embed=self.embed, view=self)

        await interaction.response.send_message(embed=embed, view=Controller(embed, settings), ephemeral=True)


async def setup(Bot):
    await Bot.add_cog(Settings(Bot))