import discord, os, json, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):
    Bot.command_info.update({"allowance":{
        "aliases":["allowance"],
        "syntax":"",
        "usage":"Requests your daily allowance of simoleans.",
        "category":"economy"
    }})
    @commands.command(name="allowance")
    async def _allowance(ctx):
        with open(os.getcwd()+"/Recources/json/command_cooldowns.json") as file:
            cooldowns_json = json.loads(file.read())

        timedelta = database_utils.fetch_timedelta(ctx.author.id, "allowance")

        if timedelta < cooldowns_json["allowance"]:
            res_title = random.choice(["Your parents say no.", "You have already had your daily allowance!", "You have already collected your daily simoleans."])
            res_desc = f"Try waiting roughly {int((cooldowns_json['allowance']-timedelta)/60/60)} more hour{'s' if int((cooldowns_json['allowance']-timedelta)/60/60) > 1 else ''}."
        else:
            database_utils.refresh_cooldown(ctx.author.id, "allowance")
            pay_amount = 1500+(100*database_utils.fetch_coolness(ctx.author.id)[1])
            res_title = random.choice(["Your parents hand you your daily allowance.", "You are handed your allowance.", "You get your daily allowance of simoleans."])
            res_desc = f"+{pay_amount} <:Simolean:769845739043684353> Simoleon{'s' if pay_amount != 1 else ''}"
            database_utils.alter_balance(ctx.author.id, pay_amount)

        allowance_embed = discord.Embed(title=res_title)
        if res_desc != None:
            allowance_embed.description = res_desc
        allowance_embed = general_utils.format_embed(ctx.author, allowance_embed)

        await ctx.send(embed=allowance_embed)

    Bot.add_command(_allowance)