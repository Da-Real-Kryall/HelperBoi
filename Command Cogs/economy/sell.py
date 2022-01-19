import discord, json, os, asyncio, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"sell":{
        "aliases":["sell"],
        "syntax":"<item> [amount]",
        "usage":"Will sell the specified item from your inventory. You must already have the item in your inventory (obviously), and to sell all of the specified item you can give 'all' as the amount, instead of a specific number.",
        "category":"economy"
    }})
    @commands.command(name="sell")
    async def _sell(ctx, *, args):

        error_embed = general_utils.error_embed(Bot, ctx, ctx.author, "Please provide a valid item name, followed by a valid positive integer if you wish to sell more than one item.")
        
        args = args.split(" ")
        if general_utils.represents_int(args[-1]):
            if int(args[-1]) < 1:# and ctx.author.id != general_utils.bot_owner_id:
                await ctx.send(embed=error_embed)
                return
            else:
                amount = int(args[-1])
                item_name = ' '.join(args[:-1])
        elif general_utils.represents_int(args[-1]) == False:
            if args[-1] == 'all':
                item_name = ' '.join(args[:-1])
                amount = 'all'
            else:
                amount = 1
                item_name = ' '.join(args)

        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())

        for key, value in item_json.items():
            if item_name.lower() == value["display_name"].lower():
                cur_items = database_utils.fetch_inventory(ctx.author.id, False, key)
                if amount == 'all':
                    delta = 0 - cur_items
                    amount = -delta
                elif int(amount) > cur_items:# and ctx.author.id != general_utils.bot_owner_id:
                    await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "You cant sell what you dont have!"))
                    return
                else:
                    delta = 0 - int(amount)
                sell_value = item_json[key]['value']*int(amount)

                await ctx.send(embed=discord.Embed(title=f"Confirmation: Do you want to sell {'all your' if amount == cur_items else amount} {general_utils.item_plural(value, 2 if amount == cur_items else amount)} for §{sell_value}?", colour=general_utils.Colours.yellow))
                
                check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]

                try:
                    msg = await Bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("nevermind...")
                    return
                
                if msg.content.lower() in ["yes", "ye", "yep", "yeah", "confirm", "affirmative", "true"]:
                    if int(amount) > database_utils.fetch_inventory(ctx.author.id, False, key):# and ctx.author.id != general_utils.bot_owner_id:
                        await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "You cant sell what you dont have!"))
                        return
                    database_utils.alter_items(ctx.author.id, "delta", {key: delta})
                    database_utils.alter_balance(ctx.author.id, sell_value)

                    sold_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Sold {amount} {general_utils.item_plural(value, amount)} for §{sell_value}."))
                    sold_embed.description = f"{'+' if delta > -1 else ''}{delta} {value['emoji']} {value['display_name']}\n{'+' if sell_value > -1 else ''}{sell_value} <:Simolean:769845739043684353> Simoleon{'s' if sell_value != 1 else ''}"
 
                    await ctx.send(embed=sold_embed)
                    return
                elif msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
                    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
                    return

        await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"{item_name} isnt a valid item!"))

    Bot.add_command(_sell)