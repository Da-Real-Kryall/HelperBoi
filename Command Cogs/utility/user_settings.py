import discord, json, os
from utils import database_utils, general_utils
from discord.ext import menus, commands

def setup(Bot):

    Bot.command_info.update({"user_settings":{
        "aliases":["user_settings", "user_preferences"],
        "syntax":"",
        "usage":"Will open a GUI for editing personal settings.",
        "category":"utility"
    }})

    with open(os.getcwd()+"/Recources/json/settings_key.json") as file:
        settings_json = json.loads(file.read())

    #up     "\N{UPWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"
    #down   "\N{DOWNWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"
    #toggle "\N{RADIO BUTTON}"
    #reset  "\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}"
    #done   "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}"


    class SettingsMenu(menus.Menu):

        async def send_initial_message(self, ctx, channel): #treating this as an init, making a proper init func breaks the assuming to be preexisting one.
            self.settings_list = {}
            self.scroll_index = 0
            self.author = ctx.author
            def _create_embed(author, settings_list, scroll_index):
                embed = discord.Embed(title=f"{author}'s Personal Preferences:", colour=general_utils.Colours.main)

                settings_list_string = [f"`   ` { {0:':no_entry:',1:':white_check_mark:'}[value]} `{setting}`" for setting, value in self.settings_list.items()]
                settings_list_string[self.scroll_index] = "` >"+settings_list_string[self.scroll_index][3:]

                embed.description = "\n".join(settings_list_string)

                embed.add_field(name="Option Effect:", value=settings_json["users"][list(self.settings_list.items())[self.scroll_index][0]]["description"])

                return embed
            
            self.create_embed = _create_embed

            for setting in settings_json["users"].keys():
                self.settings_list.update({setting: database_utils.fetch_setting("users", self.author.id, setting)})

            return await channel.send(embed=self.create_embed(self.author.display_name, self.settings_list, self.scroll_index))

            
        @menus.button("\N{RADIO BUTTON}")
        async def on_radio_button_down(self, payload):
            setting = list(self.settings_list.items())[self.scroll_index][0]
            current_value = self.settings_list[setting]

            database_utils.alter_setting("users", self.author.id, setting, 1 if current_value == 0 else 0)

            self.settings_list[setting] = 0 if current_value == 1 else 1

            await self.message.edit(embed=self.create_embed(self.author.display_name, self.settings_list, self.scroll_index))

        
        @menus.button("\N{UPWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}")
        async def on_arrow_up_down(self, payload):                        #lul function names

            if self.scroll_index > 0:
                self.scroll_index -= 1
            
            await self.message.edit(embed=self.create_embed(self.author.display_name, self.settings_list, self.scroll_index))


        @menus.button("\N{DOWNWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}")
        async def on_arrow_down_down(self, payload):

            if self.scroll_index < len(self.settings_list)-1:
                self.scroll_index += 1

            await self.message.edit(embed=self.create_embed(self.author.display_name, self.settings_list, self.scroll_index))


        @menus.button("\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}")
        async def on_stop(self, payload):
            self.stop()

    @commands.command(name="user_settings", aliases=["user_preferences"])
    async def _user_settings(ctx):
        
        m = SettingsMenu(clear_reactions_after=True)
        await m.start(ctx)
        
    Bot.add_command(_user_settings)
