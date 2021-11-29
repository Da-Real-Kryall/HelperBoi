import discord, os, json
from discord.ext import commands, menus
from utils import general_utils

def setup(Bot):

    with open(os.getcwd()+"/Recources/json/misc_economy.json") as file:
        shops_json = json.loads(file.read())["stores"]
    with open(os.getcwd()+"/Recources/json/items.json") as file:
        items_json = json.loads(file.read())

    class CatalogueMenu(menus.Menu):

        async def send_initial_message(self, ctx, channel): #treating this as an init, making a proper init func breaks the assuming to be preexisting one.

            self.scroll_index = 0
            
            self.store_embeds = [(discord.Embed(title=list(shops_json.values())[index]["display_name"], colour=discord.Colour(list(shops_json.values())[index]["colour"]), description=list(shops_json.values())[index]["description"]), list(shops_json.keys())[index]) for index in range(len(shops_json.items()))]

            for embed, store in self.store_embeds:
                embed_desc = []
                for item in items_json.values():
                    if item["purchasable"] != None:
                        if store == item["purchasable"]:
                            embed_desc += [f"\u200b  \u200b  {int(item['value']*1.2)} <:Simolean:769845739043684353>\u200b  \u200b  \u200b  \u200b  \u200b{item['emoji']}  {item['display_name']}"]
                embed.add_field(name="Items:", value="\n".join(embed_desc))
                embed = general_utils.format_embed(ctx.author, embed)
            def _create_embed():
                embed = self.store_embeds[self.scroll_index][0]
                
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
 
            if self.scroll_index < len(shops_json.items())-1:
                self.scroll_index += 1

            await self.message.edit(embed=self.create_embed())


        @menus.button("\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}")
        async def on_stop(self, payload):
            self.stop()


    Bot.command_info.update({"catalogue":{
        "aliases":["catalogue"],
        "syntax":"",
        "usage":"Returns a reaction-controlled GUI showing the items sold at each of the available stores.",
        "category":"economy"
    }})
    @commands.command(name="catalogue")
    async def _catalogue(ctx): 
        menu = CatalogueMenu()
        await menu.start(ctx)
        #e,n='E'*5,'\n'
        #await ctx.send(embed=discord.Embed(title=((e*3+n)*2+(e+n)*2)*2+(e*3+n)*2,colour=general_utils.Colours.main))

    Bot.add_command(_catalogue)