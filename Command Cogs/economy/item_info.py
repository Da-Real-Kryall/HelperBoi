import discord, os, json
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"item_info":{
        "aliases":["item_info", "iinfo"],
        "syntax":"<item>",
        "usage":"Gives information about the item specified.",
        "category":"economy"
    }})
    @commands.command(name="item_info", aliases=["iinfo"])
    async def _item_info(ctx, *, item_input):
        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())
        with open(os.getcwd()+"/Recources/json/misc_economy.json") as file:
            misc_economy_json = json.loads(file.read())

        for item in item_json.values():
            if item_input.lower() == item["display_name"].lower():
                item_info_embed = discord.Embed(title=f"Info about the \"{item['emoji']} {item_input}\":", description=item["description"])
                item_info_embed = general_utils.format_embed(ctx.author, item_info_embed)
                item_info_embed.add_field(name="Can be bought in:", value=misc_economy_json["stores"][item['purchasable']]['display_name'] if item['purchasable'] != None else "No stores.", inline=False)
                item_info_embed.add_field(name="Item Type:", value=item['type'], inline=False)
                item_info_embed.add_field(name="Sell Value:", value=f"§{item['value']}", inline=False)
                usability = "Cannot be used." if item['usability'] == None else (f"Can be used.{' not' if item['usability']['consumable'] == 0 else ''} consumable.")
                item_info_embed.add_field(name="Usability:", value=usability, inline=False)
                await ctx.send(embed=item_info_embed)
                return
        
        await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, f"\"{item_input}\" doesn't seem to be a valid item."))

    Bot.add_command(_item_info)