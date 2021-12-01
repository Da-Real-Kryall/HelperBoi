import discord, os, json, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    with open(os.getcwd()+"/Recources/json/command_cooldowns.json") as file:
        cooldowns_json = json.loads(file.read())

    #   [text if len(text) >= 2048 else text[:2045]+'...']

    Bot.command_info.update({"report_bug":{
        "aliases":["report_bug", "rb"],
        "syntax":"<bug info>",
        "usage":"Allows you to post reports about bugs you will definitely find when using the bot.",
        "category":"utility"
    }})
    @commands.command(name="report_bug", aliases=['rb'])
    async def _report_bug(ctx, *, text):
        timedelta = database_utils.fetch_timedelta(ctx.author.id, "bugreport")

        if timedelta < cooldowns_json["bugreport"]:
            await ctx.send(embed=general_utils.error_embed(False, f"Please wait {cooldowns_json['postsuggestion']-timedelta} more second{'s' if cooldowns_json['postsuggestion']-timedelta > 1 else ''} and try again. Sorry, this cooldown is just to help prevent abuse of the command."))
            return
        elif len(text) > 2048:
            await ctx.send(embed=general_utils.error_embed(True, f"The length of your bug report ({len(text)} characters) can't exceed 2^11 characters, please shorten the report and try again (the cooldown has not been refreshed)."))
            return

        database_utils.refresh_cooldown(ctx.author.id, "bugreport")
        database_utils.alter_bugreports({"insert":{ctx.author.id: text},"delete":[]})
        result_embed = discord.Embed(title="Your report has been recorded!")

        owner = Bot.get_user(general_utils.bot_owner_id)
        await owner.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"{ctx.author.display_name} just reported the following bug:", description=text)))

        if random.randint(1,9) == 3:
            giveamount = random.randint(2,4)
            result_embed.description = f"Have §{giveamount} as thanks!"
            database_utils.alter_balance(ctx.author.id, giveamount)
            database_utils.alter_coolness(ctx.author.id, random.randint(10,25))
            
        await ctx.send(embed=general_utils.format_embed(ctx.author, result_embed, "green"))

    Bot.add_command(_report_bug)