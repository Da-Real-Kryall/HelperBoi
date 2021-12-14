import discord, time
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    delay_dict = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 24*60*60,
        'w': 7*24*60*60,
        'M': 30*24*60*60, #idk predicting month lengths
        'y': 365*24*60*60
    }

    Bot.command_info.update({"remind":{
        "aliases":["remind"],
        "syntax":"<delay> <message>",
        "usage":"Sets a reminder with the given delay, of which should be specified as something like \"Xy,XM,Xw,Xd,Xh,Xm,Xs\".\n(X being any positive integer), each token specifying years, months, weeks, days, hours, mins etc.\nEach are optional and order doesnt matter, also dont put spaces after those commas in delay.",
        "category":"utility"
    }})
    @commands.command(name="remind")
    async def _remind(ctx, delay, *, message):
        try: #show examples in error
            delay = delay.split(',')
            delay = {token[-1]:float(token[:-1]) for token in delay}
            delay = sum([delay_dict[key]*value for key, value in delay.items()])
            if delay < 1:
                raise ValueError("final delay must be larger than 0.")
        except Exception as e:
            await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title="Error while parsing your given delay.", description=f"{e}\nSome examples of a valid delay are:\n`2h,3m` -> 2 hours and 3 minutes.\n`4d,3y` -> 3 years and 4 days.\n`3M,5s` -> (roughly) 3 months and 5 seconds."), "red"))
            return
        remind_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Set a reminder <t:{int(time.time()+delay)}:R>:", description=f"\"{message}\""))
        await ctx.send(embed=remind_embed)
        await Bot.add_reminder(message, delay, ctx.message)
    Bot.add_command(_remind)