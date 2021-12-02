#i really should clean up the code in this

import discord, json, os, asyncio, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):


    Bot.command_info.update({"trade":{
        "aliases":["trade"],
        "syntax":"<user> `<items_to_give>` `<items_to_recieve>`",
        "usage":f"Will (after confirming with both users) trade the first lot of items given for the second lot of items given, with your and the player specified's inventories. The item lots should be given as `Item name*amount+Second item name*amount+third item name*amount... etc etc`\nExcuse the jankiness with the method for specifying items, i am open for suggestions with alternate methods. (`%prefixsuggest`)\n\n__EXAMPLE:__\n%prefixtrade jeff `Food wrapper*6+Empty Can*5+apple*2` `quartz*2`",
        "category":"economy"
    }})
    @commands.command(name="trade")
    async def _trade(ctx, user, *, trade_string):

        user_ids = general_utils.get_player_id(Bot, ctx, user)
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

        items_giving = {}
        items_recieving = {}
        error_embed = general_utils.format_embed(ctx.author, discord.Embed(title="There was an error whilst parsing your given item lists:"), "red")
        trade_string = trade_string[1:-1].split("` `")
        if len(trade_string) != 2:
            error_embed.description = f"You gave {len(trade_string)} item lists, please provide only two; one for the items you wish to give, and a second one for the items you wish to recieve, each enclosed in `graves` (\`\`)"
            await ctx.send(embed=error_embed)
            return
        for item in trade_string[0].split("+"):
            item = item.split("*")
            if len(item) != 2:
                error_embed.description = f"{'*'.join(item)} was incorrectly formatted, please provide an item and quantity like so: `...+item*amount+...`"
                await ctx.send(embed=error_embed)
                return
            items_giving.update({item[0].lower(): int(item[1])})
        for item in trade_string[1].split("+"):
            item = item.split("*")
            if len(item) != 2:
                error_embed.description = f"{'*'.join(item)} was incorrectly formatted, please provide an item and quantity like so: `...+item*amount+...`"
                await ctx.send(embed=error_embed)
                return
            items_recieving.update({item[0].lower(): int(item[1])})

        #make a list of all valid item names, for reference when checking validity of given items
        item_reference = {}
        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())

        for key, value in item_json.items(): #heh items.items
            item_reference.update({value["display_name"].lower(): key})

        #check if all the items are valid
        for item in items_recieving.keys():
            #print(item.lower(), item_reference.keys())
            if item.lower() not in item_reference.keys():
                error_embed.description = f"'{item}' is not a valid item name. Note that spaces in item names are accepted and shouldnt be swapped with underscores, also the names are case-insensitive (you can use all caps and it wont care)"
                await ctx.send(embed=error_embed)
                return
    
        for item in items_giving.keys():
            if item.lower() not in item_reference.keys():
                error_embed.description = f"'{item}' is not a valid item name. Note that spaces in item names are accepted and shouldnt be swapped with underscores, also the names are case-insensitive (you can use all caps and it wont care)"
                await ctx.send(embed=error_embed)
                return

        #check if both users have the items

        #<confirm author agrees with trade>
        confirm_embed = discord.Embed(title=f"Confirmation: {ctx.author.name}, do you really want to trade this?", colour=general_utils.Colours.yellow)
        author_getting = []
        for item, amount in items_giving.items():
            item = item_json[item_reference[item]]
            author_getting += [f"{'+' if amount > -1 else ''}{amount} {item['emoji']} {item['display_name']}{item['plural'] if amount != 1 else ''}"]
        for item, amount in items_recieving.items():
            item = item_json[item_reference[item]]
            author_getting += [f"{'+' if -amount > -1 else ''}{-amount} {item['emoji']} {item['display_name']}{item['plural'] if -amount != 1 else ''}"]
        confirm_embed.add_field(name=f"{ctx.author.name} Recieves:", value="\n".join(author_getting))

        recipient = await ctx.guild.fetch_member(user_id)

        recipient_getting = []
        for item, amount in items_giving.items():
            item = item_json[item_reference[item]]
            recipient_getting += [f"{'+' if -amount > -1 else ''}{-amount} {item['emoji']} {item['display_name']}{item['plural'] if -amount != 1 else ''}"]
        for item, amount in items_recieving.items():
            item = item_json[item_reference[item]]
            recipient_getting += [f"{'+' if amount > -1 else ''}{amount} {item['emoji']} {item['display_name']}{item['plural'] if amount != 1 else ''}"]
        confirm_embed.add_field(name=f"{recipient.name} Recieves:", value="\n".join(recipient_getting))
        await ctx.send(embed=confirm_embed)

        check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]
        try:
            msg = await Bot.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("nevermind...")
            return
        if msg.content.lower() in ["yes", "ye", "yep", "yeah", "confirm", "affirmative", "true"]:
            #await ctx.send("okie...")

            author_current_items = database_utils.fetch_inventory(ctx.author.id)
            #print(item_reference)
            #print(author_current_items)
            #print(items_giving)
            #print(items_recieving)
            for item, amount in author_current_items.items():
                #print(item, amount)
                if item_json[item]["display_name"].lower() in list(items_giving.keys()):
                    if items_giving[item_json[item]["display_name"].lower()] > amount:
                        await ctx.send(embed=general_utils.error_embed(False, f"You cant trade what you dont have!"+(f"\n You attempted to give {items_giving[item_json[item]['display_name'].lower()]} {item_json[item]['emoji']} {item_json[item]['display_name']}{value['plural'] if items_giving[item_json[item]['display_name'].lower()] else ''} despite only having {amount} in your inventory. " if database_utils.fetch_setting("users", user_id, "economy_invisibility") == False else "")))
                        return
                    elif items_giving[item_json[item]["display_name"].lower()] < 1:
                        await ctx.send(embed=general_utils.error_embed(False, f"You cannot trade a negative item amount!"))
                        return

            #await ctx.send("I'll now confirm the recipient also wants to trade.")

        elif msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
            await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
            return

        #first check the author

        #<confirm recipient agrees with trade>

        confirm_embed.title = f"Confirmation: {recipient.name}, do you really want to trade this?"
        await ctx.send(embed=confirm_embed)
        
        check = lambda m: m.channel == ctx.message.channel and m.author == recipient and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]
        
        try:
            msg = await Bot.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("nevermind...")
            return
        
        #if msg.content.lower() in ["yes", "ye", "yep", "yeah", "confirm", "affirmative", "true"]:
        #    pass#await ctx.send("okie.")

        if msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
            await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
            return

        #then AFTER the second user confirms say wether they have enough; to prevent exposing the inventory of someone with economic invisibility turned on
        recipient_current_items = database_utils.fetch_inventory(user_id)
        for item, amount in recipient_current_items.items():
            if item_json[item]["display_name"].lower() in list(items_recieving.keys()):
                #print('test')
                if items_recieving[item_json[item]["display_name"].lower()] > amount:
                    #print('test2')
                    await ctx.send(embed=general_utils.error_embed(False, f"You cant trade what the other person doesnt have!"+(f"\n You attempted to trade {items_recieving[item_json[item]['display_name'].lower()]} {item_json[item]['emoji']} {item_json[item]['display_name']}{value['plural'] if items_recieving[item_json[item]['display_name'].lower()] else ''} despite them only having {amount} in their inventory. " if database_utils.fetch_setting("users", user_id, "economy_invisibility") == False else "")))
                    return
                elif items_recieving[item_json[item]["display_name"].lower()] < 1:
                    #print('test3')
                    await ctx.send(embed=general_utils.error_embed(False, f"You cannot trade a negative item amount!"))
                    return
        #await ctx.send(f"you will be giving {items_giving} for {items_recieving}")

        #excuse the hardcoding
        #applying the inventory changes for the trade
        database_utils.alter_items(ctx.author.id, "delta", {item_reference[name]: -amount for name, amount in items_giving.items()})
        database_utils.alter_items(ctx.author.id, "delta", {item_reference[name]: amount for name, amount in items_recieving.items()})
        database_utils.alter_items(recipient.id, "delta", {item_reference[name]: -amount for name, amount in items_recieving.items()})
        database_utils.alter_items(recipient.id, "delta", {item_reference[name]: amount for name, amount in items_giving.items()})

        success_embed = general_utils.format_embed(ctx.author, discord.Embed(title="Trade successful!"), "green")
        success_embed.add_field(name=f"{ctx.author.name} Recieved:", value="\n".join(author_getting))
        success_embed.add_field(name=f"{recipient.name} Recieved:", value="\n".join(recipient_getting))
        
        await ctx.send(embed=success_embed)
        

    Bot.add_command(_trade)