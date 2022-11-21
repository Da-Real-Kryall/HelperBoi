import re, os, json, random
from asyncio import sleep
from utils import database_utils

async def setup(Bot):

    #(?i)\bi\'m\b|\bim\b|\bi am\b
    #(?i)(\b[\w|\s]+\b)

    with open(os.getcwd()+"/Resources/json/dad_jokes.json") as file:
        dad_jokes_json = json.loads(file.read())


    @Bot.listen()
    async def on_message(message):

        if message.guild != None: #seperate to avoid errors with database_utils.fetch_setting
            if message.author.bot == False and database_utils.fetch_guild_settings(message.guild.id)["dad_jokes"] == True:

                #try the hi hungry im dad
                if random.randint(1, 6) == 2:
                    exp = r"(?i)\bi\'m\b|\bim\b|\bi am\b" #im sure this can be shortened
                    m = re.search(exp, message.content)
                    if m != None:
                        exp2 = r"(?i)(\b[\w|\s]+\b)"
                        m2 = re.search(exp2, message.content[m.end():])
                        if m2 != None:
                            await message.channel.send(f"Hi {m2.group(0)}, I'm dad!")
                            return
                
                #try autoresponses
                if message.content.lower().replace("'", "") in dad_jokes_json["responses"]:
                    msg = dad_jokes_json["responses"][message.content.lower().replace("'", "")]
                    if random.randint(1,3) == 1: msg = msg.capitalize()
                    if random.randint(1,3) == 1 and msg[-1] not in ['!', '?']: msg = msg+'.'
                    await message.channel.send(msg)
                    return

                #try spontaneous responses
                if random.randint(1,1000) == 241:
                    for msg in random.choice(dad_jokes_json["spontaneous"]):
                        await sleep(random.randint(9,15)/10)
                        if random.randint(1,3) == 1: msg = msg.capitalize()
                        if random.randint(1,3) == 1 and msg[-1] not in ['!', '?']: msg = msg+'.'
                        await message.channel.send(msg)
                    return

    print("Dad jokes loaded!")