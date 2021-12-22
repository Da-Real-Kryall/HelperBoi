from utils import database_utils
from random import randint
def setup(Bot):
    #on_message event for giving exp
    @Bot.listen()
    async def on_message(message):
        if message.author.bot == False:
            level = database_utils.fetch_coolness(message.author.id)[1] #*level
            
            database_utils.alter_coolness(message.author.id, randint(4,8))
             
            newlevel = database_utils.fetch_coolness(message.author.id)[1]
            if newlevel != level:
                if database_utils.fetch_setting("users", message.author.id, 'level_up_alert') == True:
                    if newlevel > level:
                        await message.channel.send(f"{':tada: ' if randint(1,3) == 3 else ''}{message.author.name}, your coolness is now level {newlevel}. :sunglasses:")
                    elif newlevel < level:
                        await message.channel.send(f"{':confused: ' if randint(1,3) == 3 else ''}{message.author.name}, your coolness has decreased to level {newlevel}...")
