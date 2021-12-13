import discord, random
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    cmd_dict = { #& means random user
        "rcol": {"amount": str(random.randint(1,10)), "mode": str(random.choice(['vibrant', 'normal', 'greyscale']))},
        "frg": {},
        "scng": {},
        "geoforecast":{},
        "pat": {"user": "&"},
        "boop": {"user": "&"},
        "cuddle": {"user": "&"},
        "hug": {"user": "&"},
        "pastafarian_holiday": {},
        "hello": {},
        "brocode": {},
        "scp": {},
        "rickroll": {},
        "randname": {"count": str(random.randint(1, 10))},
        "e": {},
        "coinflip": {},
        "bored": {},
        "asciilist": {}
    }

    Bot.command_info.update({"randfun":{
        "aliases":["randfun", "rf"],
        "syntax":"",
        "usage":"Runs a random fun command with semi random command arguments. For funzies and hopefully no repercussions!",
        "category":"fun"
    }})
    @commands.command(name="randfun", aliases=["rf"])
    async def _randfun(ctx):
        command = random.choice(list(cmd_dict.items()))
        args = {}
        args.update({"ctx": ctx})
        for name, value in command[1].items():
            args.update({name: value.replace('&', (random.choice([user.name for user in ctx.guild.members]) if ctx.guild != None else ''))})
        command = Bot.get_command(command[0])
        await command.can_run(ctx)
        await command(**args)
    Bot.add_command(_randfun)