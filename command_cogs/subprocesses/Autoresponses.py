import discord, os, json, random#
from discord.ext import commands#
from discord import app_commands#
from utils import database_utils# lol same length

# if autoresponses_require_ping is false AND the chance roll is good, then go
# or, if the setting is true, then check for a ping, and go


async def setup(Bot):
    @Bot.listen()
    async def on_message(message):
        if message.guild != None and message.author != Bot.user:
            require_ping = database_utils.fetch_guild_settings(message.guild.id)["autoresponses_require_ping"]

            if Bot.user not in message.mentions and require_ping is True:
                return

            # we can assume that the bot was pinged, or that the setting is false

            with open(os.getcwd()+"/Resources/json/autoresponses.json") as file:
                data = json.loads(file.read())

            for word in message.content.split(" "):
                if word in data["directs"] and (random.randint(0, 5) == 1 or require_ping is True):
                    response = data["responses"][data["directs"][word]]
                    
                    await message.reply(response["msg"] if response["msg"] != "" else None, file=discord.File(f"{os.getcwd()}/Resources{response['fp']}") if response['fp'] != '' else None)
                    
                    if require_ping is False:
                        break
    
    print("Autoresponses loaded!")