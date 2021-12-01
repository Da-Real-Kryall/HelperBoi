#YES this is janky, but only one person will ever be using it.

import discord
from discord.ext import commands, menus
from utils import general_utils, database_utils

def setup(Bot):


    Bot.command_info.update({"fetch_suggestions":{
        "aliases":["fetch_suggestions", "fetch_sg"],
        "syntax":"<mode> <integer>",
        "usage":"Owner only, fetches suggestions based on the arguments given.",
        "category":"hidden"
    }})

    @commands.is_owner()
    @commands.command(name="fetch_suggestions", aliases=['fetch_sg'])
    async def _fetch_suggestions(ctx, mode, integer='1'):
        
        if not general_utils.represents_int(integer):
            await ctx.send(embed=general_utils.error_embed(False, "Please pick a valid positive integer as the 'integer' argument"))
            return

        integer = int(integer)

        if mode not in ["all", "primary_key", "user", "latest"]:
            await ctx.send(embed=general_utils.error_embed(False, "Please pick either 'all', 'primary_key', 'user' or 'latest' for the mode argument."))
            return

        suggestions = database_utils.fetch_suggestions(mode,integer)

        class SuggestMenu(menus.Menu):

            async def send_initial_message(self, ctx, channel): #treating this as an init, making a proper init func breaks the assuming to be preexisting one.

                self.scroll_index = 0
                
                self.suggestion_embeds = [] if len(suggestions) != 0 else [general_utils.format_embed(ctx.author, discord.Embed(title="No suggestions exist that meet the given criteria."), general_utils.Colours.charcoal)]

                for suggestion in suggestions:
                    author = await Bot.fetch_user(suggestion[1])
                    self.suggestion_embeds += [general_utils.format_embed(ctx.author, discord.Embed(title=f"(ID: {suggestion[0] if mode != 'primary_key' else int(integer)}) Posted by {author.name} <t:{suggestion[3]}:R>: ({len(self.suggestion_embeds)+1}/{len(suggestions)})", description=suggestion[2]))]

                def _create_embed():
                    embed = self.suggestion_embeds[self.scroll_index]
                    
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
    
                if self.scroll_index < len(suggestions)-1:
                    self.scroll_index += 1

                await self.message.edit(embed=self.create_embed())

            @menus.button("\N{COLLISION SYMBOL}")
            async def on_boom_down(self, payload):
    
                database_utils.alter_suggestions({"delete":[suggestions[self.scroll_index][0] if mode != 'primary_key' else int(integer)],"insert":{}})
                new_embed = self.suggestion_embeds[self.scroll_index]
                new_embed.description = "~~"+new_embed.description+"~~"
                new_embed.title = new_embed.title[:-1]+", DELETED)"
                new_embed.colour = general_utils.Colours.red
                self.suggestion_embeds[self.scroll_index] = new_embed

                await self.message.edit(embed=self.create_embed())


            @menus.button("\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}")
            async def on_stop(self, payload):
                self.stop()

        menu = SuggestMenu(clear_reactions_after=True)
        await menu.start(ctx)
            
        #await ctx.send(embed=general_utils.format_embed(ctx.author, result_embed, "green"))

    Bot.add_command(_fetch_suggestions)