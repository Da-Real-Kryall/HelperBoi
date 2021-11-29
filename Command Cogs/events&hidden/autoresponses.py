import discord, os, string, json, random
from utils import database_utils

def setup(Bot):

    #autoresponses to messages, if the settings allow for it or if the bot was also pinged
    
    @Bot.listen()
    async def on_message(message):

        if Bot.user in message.mentions:
            wordlist = message.content.split(" ")
            if f"<@!{Bot.user.id}>" in wordlist or f"<@{Bot.user.id}>" in wordlist:
                
                with open(os.getcwd()+"/Recources/json/autoresponses.json") as file:
                    data = json.loads(file.read())
                
                for word in wordlist[:10]:
                    if word in data["directs"]:
                        response = data["responses"][data["directs"][word]]
                        await message.channel.send(response["msg"] if response["msg"] != "" else None, file=discord.File(f"{os.getcwd()}/Recources{response['fp']}") if response['fp'] != '' else None)
        
        elif database_utils.fetch_setting("servers", message.guild.id, "autoresponses_require_ping") == False:


            wordlist = message.content.split(" ")

            with open(os.getcwd()+"/Recources/json/autoresponses.json") as file:
                data = json.loads(file.read())

            for word in wordlist[:10]:
                if word in data["directs"]:
                    if random.randint(1,5) == 3:
                        response = data["responses"][data["directs"][word]]
                        await message.channel.send(response["msg"] if response["msg"] != "" else None, file=discord.File(f"{os.getcwd()}/Recources{response['fp']}") if response['fp'] != '' else None)
    