import discord, asyncio, json, os
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
        if user == None:
            user_id = int(ctx.author.id)
        else:
            user_ids = general_utils.get_player_id(False, ctx, user)
            if len(user_ids) == 0:
                await ctx.send(embed=general_utils.error_embed(False, "That isnt a member's name!"))
                return
            elif len(user_ids) > 1:
                await ctx.send("Please say the number corresponding to whichever of the possible users you meant:\n"+'\n'.join([f"[{index}] \"{str(ctx.guild.get_member(value))}\"" for index, value in enumerate(list(user_ids.keys()))]))
                
                check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author

                try:
                    msg = await Bot.wait_for('message', timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("nevermind...")
                
                id_list = [value for value in list(user_ids.keys())]

                if general_utils.represents_int(msg.content):
                    if int(msg.content) < len(id_list):
                        user_id = [value for value in list(user_ids.keys())][int(msg.content)]
                    else:
                        await ctx.send(embed=general_utils.error_embed(False, "Please pick a number that was listed."))
                        return
                else:
                    await ctx.send(embed=general_utils.error_embed(False, "Please pick a number that was listed."))
                    return
            else:
                user_id = int(list(user_ids.keys())[0])
        
        if database_utils.fetch_setting("users", user_id, "economy_invisibility") == True and ctx.author.id != user_id:
            await ctx.send(general_utils.error_embed(True, "This person has activated their economic invisibility; only they can view their inventory."))
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
        #await ctx.send("your inventory:")
        #e,n='E'*5,'\n'
        #await ctx.send(embed=discord.Embed(title=((e*3+n)*2+(e+n)*2)*2+(e*3+n)*2,colour=general_utils.Colours.main))

    Bot.add_command(_inventory)