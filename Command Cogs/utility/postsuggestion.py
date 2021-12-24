import discord, os, json, random
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    with open(os.getcwd()+"/Recources/json/command_cooldowns.json") as file:
        cooldowns_json = json.loads(file.read())

    #   [text if len(text) >= 2048 else text[:2045]+'...']

    Bot.command_info.update({"postsuggestion":{
        "aliases":["postsuggestion", "ps", "suggest"],
        "syntax":"<text in suggestion>",
        "usage":"Allows you to post feedback and suggestions for improvements/new features to be added to the bot! also, emphasis on please do not spam this command or try to abuse it.",
        "category":"utility"
    }})
    @commands.command(name="postsuggestion", aliases=['ps', "suggest"])
    async def _postsuggestion(ctx, *, text):
        #if ctx.author.id == 517371142508380170:
        #    await ctx.send("no")
        #    return
        timedelta = database_utils.fetch_timedelta(ctx.author.id, "postsuggestion")

        if timedelta < cooldowns_json["postsuggestion"]:
            await ctx.send(embed=general_utils.error_embed(False, f"Please wait {cooldowns_json['postsuggestion']-timedelta} more second{'s' if cooldowns_json['postsuggestion']-timedelta > 1 else ''} and try again. Sorry, this cooldown is just to help prevent abuse of the command."))
            return

        elif len(text) > 2048:
            await ctx.send(embed=general_utils.error_embed(True, f"The length of your suggestion ({len(text)} characters) can't exceed 2^11 characters, please shorten it and try again (the cooldown has not been refreshed)."))
            return

        database_utils.refresh_cooldown(ctx.author.id, "postsuggestion")
        database_utils.alter_suggestions({"insert":{ctx.author.id: text},"delete":[]})
        result_embed = discord.Embed(title="Your suggestion has been recorded!")

        owner = Bot.get_user(general_utils.bot_owner_id)
        await owner.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"{ctx.author.display_name} just posted a suggestion:", description=text)))

        if random.randint(1,9) == 3:
            giveamount = random.randint(2,4)
            result_embed.description = f"Have §{giveamount} as thanks!"
            database_utils.alter_balance(ctx.author.id, giveamount)
            giveamount = random.randint(10,25)
            cur_amount = database_utils.alter_coolness(ctx.author.id, giveamount)[0]
            await general_utils.level_check(giveamount, cur_amount, ctx.channel, ctx.author)

        await ctx.send(embed=general_utils.format_embed(ctx.author, result_embed, "green"))

    Bot.add_command(_postsuggestion)