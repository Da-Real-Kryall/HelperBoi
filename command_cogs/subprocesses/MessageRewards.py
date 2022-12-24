import discord, os, asyncio, random, math
from utils import general_utils, database_utils
from discord.ext import commands
from discord import app_commands

async def setup(Bot):
    @Bot.listen()
    async def on_message(message):
        if message.author.bot == True:
            return
        
        #add exp
        give_amount = random.randint(4,8)
        cur_amount = database_utils.fetch_user_data(message.author.id, "coolness")
        database_utils.set_user_data(message.author.id, "coolness", cur_amount+give_amount)

        level = math.floor(general_utils.exp_to_level(cur_amount))
        new_level = math.floor(general_utils.exp_to_level(cur_amount+give_amount))
        
        #level up alert
        if database_utils.fetch_user_data(message.author.id, "settings")["level_up_alert"] == True:
            emoji = ':sunglasses:' if new_level >= 10 else ('' if new_level in range(0,11) else ':nerd:')
            if level < new_level:
                await message.reply(embed=general_utils.Embed(author=message.author, title=f"You just reached coolness level {new_level}! {emoji}", colour="random"))
            elif level > new_level:
                await message.reply(embed=general_utils.Embed(author=message.author, title=f"Your coolness level decreased to {level}... :confused:", colour="red"))

        #money
        if random.randint(0, 4) != 0:
            return

        give_amount = random.randint(int(level/2), int(1+level*1.5))
        cur_amount = database_utils.fetch_user_data(message.author.id, "balance")
        database_utils.set_user_data(message.author.id, "balance", cur_amount+give_amount)