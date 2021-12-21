import discord, time
from discord.ext import commands, menus
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"reminders":{
        "aliases":["reminders", "view_reminders", "delete_reminders"],
        "syntax":"",
        "usage":"Returns a paginated reaction menu that allows you to view and delete set reminders",
        "category":"utility"
    }})
    @commands.command(name="reminders", aliases=["view_reminders", "delete_reminders"])
    async def _reminders(ctx):
        reminders = database_utils.fetch_reminders(ctx.author.id)
        if len(reminders) == 0:
            await ctx.send(embed=discord.Embed(title="You havent set any reminders, there are none to show.", description=f"You use this command to browse and delete set reminders, use the `remind` command to set some reminders."))
            return
        class RemindersMenu(menus.Menu):

            async def send_initial_message(self, ctx, channel): #treating this as an init, making a proper init func breaks the assuming to be preexisting one.

                self.scroll_index = 0
                
                self.reminder_embeds = [general_utils.format_embed(ctx.author, discord.Embed(title="Reminders:", description="\n".join([f"` {'>' if _index == index else ' '} ` **#{_reminder[0]}**: Set for <t:{_reminder[2]}> (<t:{_reminder[2]}:R>)" for _index, _reminder in enumerate(reminders)]))) for index, reminder in enumerate(reminders)]
                [self.reminder_embeds[index].add_field(name="Text:", value=reminder[1]) for index, reminder in enumerate(reminders)]

                return await channel.send(embed=self.reminder_embeds[self.scroll_index])


            @menus.button("\N{UPWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}")
            async def on_up_arrow_down(self, payload):

                if self.scroll_index > 0:
                    self.scroll_index -= 1
                
                await self.message.edit(embed=self.reminder_embeds[self.scroll_index])


            @menus.button("\N{DOWNWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}")
            async def on_down_arrow_down(self, payload):
    
                if self.scroll_index < len(self.reminder_embeds)-1:
                    self.scroll_index += 1

                await self.message.edit(embed=self.reminder_embeds[self.scroll_index])

            @menus.button("\N{WASTEBASKET}\N{VARIATION SELECTOR-16}")
            async def on_trash(self, payload):
                if self.reminder_embeds[self.scroll_index].colour.value != general_utils.Colours.red:
                    database_utils.remove_reminders([reminders[self.scroll_index][0]])
                    new_embed = self.reminder_embeds[self.scroll_index]
                    new_embed_desc = new_embed.description.split("\n")
                    new_embed_desc[self.scroll_index] = f"~~{new_embed_desc[self.scroll_index]}~~ (Deleted)"
                    new_embed.description = "\n".join(new_embed_desc)
                    new_embed.colour = general_utils.Colours.red
                    self.reminder_embeds[self.scroll_index] = new_embed

                    await self.message.edit(embed=self.reminder_embeds[self.scroll_index])

            @menus.button("\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}")
            async def on_stop(self, payload):
                self.stop()

        menu = RemindersMenu(clear_reactions_after=True)
        await menu.start(ctx)

    Bot.add_command(_reminders)