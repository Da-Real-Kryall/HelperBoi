import discord, json, os
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"inventory":{
        "aliases":["inventory", "inv"],
        "syntax":"[user]",
        "usage":"Will return either your inventory, or the inventory of the user given.",
        "category":"economy"
    }})
    @commands.command(name="inventory", aliases=["inv"])
    async def _inventory(ctx, *, user=None):
        user_id = await general_utils.get_user_id(Bot, ctx, user, False)
        if user_id == None:
            return
        user = await Bot.fetch_user(user_id)
        if user.bot:
            await ctx.send(embed=general_utils.error_embed(True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
            return
        
        if database_utils.fetch_setting("users", user_id, "economy_invisibility") == True and ctx.author.id != user_id:
            await ctx.send(embed=general_utils.error_embed(True, "This person has activated their economic invisibility; only they can view their inventory."))
            return

        inv_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"{ctx.guild.get_member(user_id).display_name}'s Inventory:"))

        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())

        inv_data = database_utils.fetch_inventory(user_id, True)
        inventory_string = ""
        for item, quantity in inv_data.items():
            if quantity != 0:
                inventory_string += f"\n{item_json[item]['emoji']} {item_json[item]['display_name']} x{quantity}"

        inv_embed.description = inventory_string

        await ctx.send(embed=inv_embed)

    Bot.add_command(_inventory)