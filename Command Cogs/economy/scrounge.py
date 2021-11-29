import discord, os, json, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):
    Bot.command_info.update({"scrounge":{
        "aliases":["scrounge", "scng"],
        "syntax":"",
        "usage":"Lets you scrounge in the surrounding natural environment for things on the ground that may be of value.",
        "category":"economy"
    }})
    @commands.command(name="scrounge", aliases=["scng"])
    async def _scrounge(ctx):
        with open(os.getcwd()+"/Recources/json/misc_economy.json") as file:
            misc_economy_json = json.loads(file.read())
        with open(os.getcwd()+"/Recources/json/command_cooldowns.json") as file:
            cooldowns_json = json.loads(file.read())
        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())
        scrounging_weights = misc_economy_json["scrounge_data"]["weights"]
        scrounging_result = random.choices(population=list(scrounging_weights.keys()), weights=list(scrounging_weights.values()), k=1)[0]

        timedelta = database_utils.fetch_timedelta(ctx.author.id, "scrounge")

        if timedelta < cooldowns_json["scrounge"]:
            res_title = random.choice(misc_economy_json["scrounge_data"]["messages"]["faliure"])
            res_desc = f"Try waiting {cooldowns_json['scrounge']-timedelta} more second{'s' if cooldowns_json['scrounge']-timedelta > 1 else ''}."
        elif scrounging_result == "NOTHING":
            database_utils.refresh_cooldown(ctx.author.id, "scrounge")
            res_title = random.choice(misc_economy_json["scrounge_data"]["messages"]["faliure"])
            if random.randint(1,5) == 1:
                res_desc = ":("
            else:
                res_desc = None
        elif scrounging_result == "MONEY":
            res_title = random.choice(misc_economy_json["scrounge_data"]["messages"]["success"]).replace("%", random.choice(misc_economy_json["scrounge_data"]["name_choices"][scrounging_result]))
            database_utils.refresh_cooldown(ctx.author.id, "scrounge")
            give_amount = random.randint(2, 6)
            res_desc = f"+{give_amount} <:Simolean:769845739043684353> Simoleons"
            database_utils.alter_balance(ctx.author.id, give_amount)
        else:
            database_utils.refresh_cooldown(ctx.author.id, "scrounge")
            res_title = random.choice(misc_economy_json["scrounge_data"]["messages"]["success"]).replace("%", random.choice(misc_economy_json["scrounge_data"]["name_choices"][scrounging_result]))
            res_desc = f"+1 {item_json[scrounging_result]['emoji']} {item_json[scrounging_result]['display_name']}"
            database_utils.alter_items(ctx.author.id, "delta", {scrounging_result: 1})

        scrounge_embed = discord.Embed(title=res_title)
        if res_desc != None:
            scrounge_embed.description = res_desc
        scrounge_embed = general_utils.format_embed(ctx.author, scrounge_embed)

        await ctx.send(embed=scrounge_embed)

    Bot.add_command(_scrounge)