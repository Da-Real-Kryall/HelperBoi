#YES this is janky, but only one person will ever be using it.

import discord
from discord.ext import commands, menus
from utils import general_utils, database_utils

def setup(Bot):


    Bot.command_info.update({"fetch_bugreports":{
        "aliases":["fetch_bugreports", "fetch_br"],
        "syntax":"<mode> <integer>",
        "usage":"Owner only, fetches bug reports based on the arguments given.",
        "category":"hidden"
    }})

    @commands.is_owner()
    @commands.command(name="fetch_bugreports", aliases=['fetch_br'])
    async def _fetch_bugreports(ctx, mode, integer='1'):
        
        if not general_utils.represents_int(integer):
            await ctx.send(embed=general_utils.error_embed(False, "Please pick a valid positive integer as the 'integer' argument"))
            return

        integer = int(integer)

        if mode not in ["all", "primary_key", "user", "latest"]:
            await ctx.send(embed=general_utils.error_embed(False, "Please pick either 'all', 'primary_key', 'user' or 'latest' for the mode argument."))
            return

        reports = database_utils.fetch_bugreports(mode,integer)

        class ReportMenu(menus.Menu):

            async def send_initial_message(self, ctx, channel): #treating this as an init, making a proper init func breaks the assuming to be preexisting one.

                self.scroll_index = 0
                
                self.report_embeds = [] if len(reports) != 0 else [general_utils.format_embed(ctx.author, discord.Embed(title="No reports exist that meet the given criteria."), general_utils.Colours.charcoal)]

                for report in reports:
                    author = await Bot.fetch_user(report[1])
                    self.report_embeds += [general_utils.format_embed(ctx.author, discord.Embed(title=f"(#{report[0]}) Posted by {author.name} <t:{report[3]}:R>:", description=report[2]))]

                def _create_embed():
                    embed = self.report_embeds[self.scroll_index]
                    
                    return embed
                self.create_embed = _create_embed

                return await channel.send(embed=self.create_embed())


            @menus.button("\N{LEFTWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}")
            async def on_arrow_left_down(self, payload):

                if self.scroll_index > 0:
                    self.scroll_index -= 1
                
                await self.message.edit(embed=self.create_embed())


            @menus.button("\N{BLACK RIGHTWARDS ARROW}\N{VARIATION SELECTOR-16}")
            async def on_arrow_right_down(self, payload):
    
                if self.scroll_index < len(reports)-1:
                    self.scroll_index += 1

                await self.message.edit(embed=self.create_embed())


            @menus.button("\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}")
            async def on_stop(self, payload):
                self.stop()

        menu = ReportMenu(clear_reactions_after=True)
        await menu.start(ctx)
            
        #await ctx.send(embed=general_utils.format_embed(ctx.author, result_embed, "green"))

    Bot.add_command(_fetch_bugreports)