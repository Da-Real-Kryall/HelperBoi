import discord, json, os, asyncio, random
from discord.ext import commands
from utils import general_utils, database_utils, use_functions

def setup(Bot):

    Bot.command_info.update({"eat":{
        "aliases":["eat"],
        "syntax":"<item> [amount]",
        "usage":"Lets you eat food items.",
        "category":"economy"
    }})
    @commands.command(name="eat")
    async def _eat(ctx, *, args):

        error_embed = general_utils.error_embed(ctx.author, "Please provide a valid item name, followed by either a valid positive integer or 'all', as the amount, if applicable.")
        
        args = args.split(" ")
        amount = ''

        if general_utils.represents_int(args[-1]) == False:
            if args[-1] == 'all':
                amount = 'all'
                item_name = ' '.join(args[:-1])
            else:
                amount = '1'
                item_name = ' '.join(args)
            #elif args[-1] != 'all':
            #    await ctx.send(embed=error_embed)
        else:
            item_name = ' '.join(args[:-1])
            amount = args[-1]

        if amount != 'all':
            if int(amount) < 1:# and ctx.author.id != general_utils.bot_owner_id:
                await ctx.send(embed=error_embed)
                return
        
        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())

        for key, value in item_json.items():
            if item_name.lower() == value["display_name"].lower():
                if value['usability'] == None or value["type"] != "Food":
                    await ctx.send(embed=general_utils.error_embed(False, "That item isnt edible! (or at least you shouldnt be eating it)"))
                    return

                cur_item_amount = database_utils.fetch_inventory(ctx.author.id, False, key)
                if amount == 'all':
                    if cur_item_amount == 0:
                        await ctx.send(embed=general_utils.error_embed(False, "You dont have any of that item!"))
                        return
                    delta = 0 - database_utils.fetch_inventory(ctx.author.id, False, key)
                    amount = -delta
                else:
                    delta = -int(amount)
                    amount = int(amount)
                if int(amount) > cur_item_amount and cur_item_amount > -1:# and ctx.author.id != general_utils.bot_owner_id:
                    await ctx.send(embed=general_utils.error_embed(False, "You cant eat what you dont have!"))
                    return

                if value['usability']['confirmation']:
                    await ctx.send(embed=discord.Embed(title=f"Confirmation: Do you want to eat {'all your' if amount == cur_item_amount else amount} {general_utils.item_plural(value, 2 if amount == cur_item_amount else amount)}?", colour=general_utils.Colours.yellow))
                    
                    check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]
                    
                    try:
                        msg = await Bot.wait_for('message', timeout=15.0, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send("nevermind...")
                        return
                    
                    if msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
                        await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
                        return
                        #elif msg.content.lower() in ["yes", "ye", "yep", "yeah", "confirm", "affirmative", "true"]:
                        #    database_utils.alter_items(ctx.author.id, "delta", {key: delta})
                        #    database_utils.alter_balance(ctx.author.id, sell_value)

                        #    sold_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Sold {amount}x {value['emoji']} {value['display_name']} for §{sell_value}"))
                        #    sold_embed.description = f"{'+' if delta > -1 else ''}{delta} {value['emoji']} {value['display_name']}{value['plural'] if amount else ''}\n{'+' if sell_value > -1 else ''}{sell_value} <:Simolean:769845739043684353> Simoleon{'s' if sell_value != 0 else ''}"

                        #    await ctx.send(embed=sold_embed)
                        #    return
                        
                cur_item_amount = database_utils.fetch_inventory(ctx.author.id, False, key)
                if int(amount) > cur_item_amount and cur_item_amount > -1:# and ctx.author.id != general_utils.bot_owner_id:
                    await ctx.send(embed=general_utils.error_embed(False, "You cant eat what you dont have!"))
                    return

                if value['usability']['consumable']:
                    database_utils.alter_items(ctx.author.id, "delta", {key: delta})

                try:
                    print(use_functions.reference)
                    await use_functions.reference["food"][value['usability']['function']](message=ctx.message, amount=int(amount))
                except RuntimeError:
                    return
                return
        await ctx.send(embed=general_utils.error_embed(False, f"{item_name} isnt a valid item!"))

    Bot.add_command(_eat)