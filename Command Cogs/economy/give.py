import discord, json, os, asyncio, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    Bot.command_info.update({"give":{
        "aliases":["give"],
        "syntax":"<user> <amount> <item>",
        "usage":"Will give the specified amount of the specified item to the specified server member. You must already have the item in your inventory (obviously), and to give all of the specified item you can give 'all' as the amount.",
        "category":"economy"
    }})
    @commands.command(name="give")
    async def _give(ctx, user, amount, *, item_name):
        error_embed = general_utils.error_embed(ctx.author, "Please give a valid positive integer or 'all' as the amount of items to give, followed by the name of the item(s) you wish to sell.")
        if general_utils.represents_int(amount):
            if int(amount) < 1 and ctx.author.id != general_utils.bot_owner_id:
                await ctx.send(embed=error_embed)
                return
        elif amount != "all":
            await ctx.send(embed=error_embed)
            return

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

        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())

        for key, value in item_json.items():
            if item_name.lower() == value["display_name"].lower():
                if amount == 'all':
                    delta = 0 - database_utils.fetch_inventory(ctx.author.id, False, key)
                elif int(amount) > database_utils.fetch_inventory(ctx.author.id, False, key) and ctx.author.id != general_utils.bot_owner_id:
                    await ctx.send(embed=general_utils.error_embed(False, "You cant sell what you dont have!"))
                    return
                else:
                    delta = 0 - int(amount)

                recipient_name = await Bot.fetch_user(user_id)
                recipient_name = recipient_name.name

                await ctx.send(embed=discord.Embed(title=f"Confirmation: Do you want to give {'all your' if amount == 'all' else amount} {value['display_name']}{'s' if amount != 1 else ''} to {recipient_name}?", colour=general_utils.Colours.yellow))
                
                check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]

                try:
                    msg = await Bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("nevermind...")
                    return
                
                if msg.content.lower() in ["yes", "ye", "yep", "yeah", "confirm", "affirmative", "true"]:
                    database_utils.alter_items(ctx.author.id, "delta", {key: delta})
                    database_utils.alter_items(user_id, "delta", {key: -delta})

                    gave_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Gave {amount}x {value['emoji']} {value['display_name']} to {recipient_name}"))
                    gave_embed.add_field(name=f"{ctx.author.name}:", value=f"{'+' if delta > -1 else ''}{delta} {value['emoji']} {value['display_name']}{value['plural'] if amount else ''}")
                    gave_embed.add_field(name=f"{recipient_name}:", value=f"{'+' if -delta > -1 else ''}{-delta} {value['emoji']} {value['display_name']}{value['plural'] if amount else ''}")
 
                    await ctx.send(embed=gave_embed)
                    return
                elif msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
                    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
                    return

        await ctx.send(embed=general_utils.error_embed(False, f"{item_name} isnt a valid item!"))

    Bot.add_command(_give)