from utils import database_utils
from random import randint
def setup(Bot):
    #on_message event for giving small amounts of money
    @Bot.listen()
    async def on_message(message):
        if randint(1,5) == 3 and message.author.bot == False:
            level = database_utils.fetch_coolness(message.author.id)[1] #*level
            reward_amount = randint(int(level/2), int(1+level*1.5))
            database_utils.alter_balance(message.author.id, reward_amount)