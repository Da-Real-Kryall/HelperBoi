import discord, json, os, asyncio, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"buy":{
        "aliases":["buy", "purchase"],
        "syntax":"<item> [amount]",
        "usage":"Will purchase the given amount of the given item from its respective store. If no amount is given, one of the given item will be bought.",
        "category":"economy"
    }})
    @commands.command(name="buy", aliases=["purchase"])
    async def _buy(ctx, *, args):

        error_embed = general_utils.error_embed(ctx.author, "Please provide a valid item name, followed by a valid positive integer if you wish to buy more than one item.")
        
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
            shops_json = json.loads(file.read())["stores"]

        for key, value in item_json.items():
            if item_name.lower() == value["display_name"].lower():
                if value["purchasable"] == None:
                    await ctx.send(embed=general_utils.error_embed(False, f"That item isn't purchasable!"))
                    return

                buy_price = amount*value["value"] #heh value[value]
                user_balance = database_utils.fetch_balance(ctx.author.id)
                if buy_price > user_balance:
                    await ctx.send(embed=general_utils.error_embed(False, f"You dont have enough money to buy that! You needed §{buy_price} to purchase this"+(f", despite having only §{user_balance}." if database_utils.fetch_setting("users", ctx.author.id, "economy_invisibility") == False else ".")))
                    return

                await ctx.send(embed=discord.Embed(title=f"Confirmation: Do you want to buy {amount if amount != 1 else 'a'} {value['display_name']}{value['plural'] if amount != 1 else ''} for §{buy_price}?", colour=general_utils.Colours.yellow))
                
                check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]

                try:
                    msg = await Bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("nevermind...")
                    return
                
                if msg.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true"]:
                    database_utils.alter_items(ctx.author.id, "delta", {key: amount})
                    database_utils.alter_balance(ctx.author.id, -buy_price)

                    bought_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Bought {amount}x {value['emoji']} {value['display_name']} from the {shops_json[value['purchasable']]['display_name']}"))
                    bought_embed.description = f"{'+' if amount > -1 else ''}{amount} {value['emoji']} {value['display_name']}{value['plural'] if amount != 1 else ''}\n{'+' if -buy_price > -1 else ''}{-buy_price} <:Simolean:769845739043684353> Simoleon{'s' if buy_price != 1 else ''}"
                    bought_embed.colour = shops_json[value['purchasable']]['colour']

                    await ctx.send(embed=bought_embed)
                    return
                elif msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
                    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
                    return

        await ctx.send(embed=general_utils.error_embed(False, f"{item_name} isnt a valid item!"))

    Bot.add_command(_buy)