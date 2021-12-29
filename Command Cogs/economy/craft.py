import discord, json, os, asyncio, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"craft":{
        "aliases":["craft"],
        "syntax":"<item> [amount]",
        "usage":"Will craft the specified amount of the specified item, given that you have the materials. and the amount is optional and will default to 1, giving 'all' as the amount will also craft the maximum amount possible with your current materials.",
        "category":"economy"
    }})
    @commands.command(name="craft")
    async def _craft(ctx, *, args):

        error_embed = general_utils.error_embed(ctx.author, "Please provide a valid item name, followed by a valid positive integer if you wish to craft more than one item, or 'all' if you want to craft as many as you possibly can.")
        
        args = args.split(" ")
        if general_utils.represents_int(args[-1]):
            if int(args[-1]) < 1 and ctx.author.id != general_utils.bot_owner_id:
                await ctx.send(embed=error_embed)
                return
            else:
                amount = int(args[-1])
                item_name = ' '.join(args[:-1])
        else:
            amount = 1
            item_name = ' '.join(args)

        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())
        with open(os.getcwd()+"/Recources/json/misc_economy.json") as file:
            misc_economy_json = json.loads(file.read())

        delta = {} #dict of items to edit the users inv of, positive item:amount and negative materials:amount

        for key, value in item_json.items():
            if item_name.lower() == value["display_name"].lower():
                if key not in misc_economy_json["crafting_recipes"].keys():
                    await ctx.send(embed=general_utils.error_embed(True, "That item isnt craftable."))
                    return
                current_inventory = database_utils.fetch_inventory(ctx.author.id, True)
                if amount == 'all':
                    amount = min([v//misc_economy_json["crafting_recipes"][key]['items'][k] for k, v in current_inventory.items()])
                    for k, v in misc_economy_json["crafting_recipes"][key]['items'].items():
                        delta.update({k: -(v*amount)})
                    delta.update({key: amount})
                    await ctx.send(f"you will be crafting {amount} {key}.")
                else:
                    amount = int(amount)
                    for k, v in misc_economy_json["crafting_recipes"][key]['items'].items():
                        delta.update({k: -(v*amount)})
                    delta.update({key: amount})

                #check if user has enough items
                for item, quantity in delta.items():
                    if quantity > current_inventory[item]:
                        await ctx.send(embed=general_utils.error_embed(False, "You don't have enough items to craft this!"))
                        return

                confirm_embed = discord.Embed(title=f"Confirmation: Do you want to craft {amount} {general_utils.item_plural(value, amount)}?", colour=general_utils.Colours.yellow)
                confirm_embed.add_field(name="Recipe:", value='\n'.join([f"{-v}x {item_json[k]['display_name']}" for k, v in delta.items() if item_json[k]['display_name'].lower() != item_name.lower()]))
                await ctx.send(embed=confirm_embed )
                check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]

                try:
                    msg = await Bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("nevermind...")
                    return
                
                if msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
                    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
                    return

                current_inventory = database_utils.fetch_inventory(ctx.author.id)
                #check if user has enough items
                for item, quantity in delta.items():
                    if quantity > current_inventory[item]:
                        await ctx.send(embed=general_utils.error_embed(False, "You don't have enough items to craft this!"))
                        return
                        
                database_utils.alter_items(ctx.author.id, "delta", delta)
                craft_desc = []
                for k, v in delta.items():
                    craft_desc += [f"{'+' if v > -1 else ''}{v} {item_json[k]['emoji']} {item_json[k]['display_name']}"]
                craft_desc = '\n'.join(craft_desc)
                crafted_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"You crafted {amount} {general_utils.item_plural(value, amount)}.", description=craft_desc), "green")
                await ctx.send(embed=crafted_embed)
                return

        await ctx.send(embed=general_utils.error_embed(False, f"{item_name} isnt a valid item!"))

    Bot.add_command(_craft)