from utils import database_utils, general_utils
from random import randint
def setup(Bot):
    #on_message event for giving exp
    @Bot.listen()
    async def on_message(message):
        if message.author.bot == False:
            giveamount = randint(4,8)
            cur_amount = database_utils.alter_coolness(message.author.id, giveamount)[0]
            await general_utils.level_check(giveamount, cur_amount, message.channel, message.author)
