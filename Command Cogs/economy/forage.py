import discord, os, json, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):
    Bot.command_info.update({"forage":{
        "aliases":["forage", "frg"],
        "syntax":"",
        "usage":"Lets you forage in the surrounding natural environment for things on the ground that may be of value.",
        "category":"economy"
    }})
    @commands.command(name="forage", aliases=["frg"])
    async def _forage(ctx):
        with open(os.getcwd()+"/Recources/json/misc_economy.json") as file:
            misc_economy_json = json.loads(file.read())
        with open(os.getcwd()+"/Recources/json/command_cooldowns.json") as file:
            cooldowns_json = json.loads(file.read())
        with open(os.getcwd()+"/Recources/json/items.json") as file:
            item_json = json.loads(file.read())
        foraging_weights = misc_economy_json["forage_data"]["weights"]
        foraging_result = random.choices(population=list(foraging_weights.keys()), weights=list(foraging_weights.values()), k=1)[0]

        timedelta = database_utils.fetch_timedelta(ctx.author.id, "forage")

        if timedelta < cooldowns_json["forage"]:
            res_title = random.choice(misc_economy_json["forage_data"]["messages"]["faliure"])
            res_desc = f"Try waiting {cooldowns_json['forage']-timedelta} more second{'s' if cooldowns_json['forage']-timedelta > 1 else ''}."
        elif foraging_result == "NOTHING":
            database_utils.refresh_cooldown(ctx.author.id, "forage")
            res_title = random.choice(misc_economy_json["forage_data"]["messages"]["faliure"])
            if random.randint(1,5) == 1:
                res_desc = ":("
            else:
                res_desc = None
        else:
            database_utils.refresh_cooldown(ctx.author.id, "forage")
            res_title = random.choice(misc_economy_json["forage_data"]["messages"]["success"]).replace("%", random.choice(misc_economy_json["forage_data"]["name_choices"][foraging_result]))
            res_desc = f"+1 {item_json[foraging_result]['emoji']} {item_json[foraging_result]['display_name']}"
            database_utils.alter_items(ctx.author.id, "delta", {foraging_result: 1})

        forage_embed = discord.Embed(title=res_title)
        if res_desc != None:
            forage_embed.description = res_desc
        forage_embed = general_utils.format_embed(ctx.author, forage_embed)

        await ctx.send(embed=forage_embed)

    Bot.add_command(_forage)