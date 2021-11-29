import discord, os
from discord.ext import commands

def setup(Bot):
    @Bot.listen()
    async def on_message(message):
        if hasattr(message.channel, "me") and message.author.id == 479963507631194133 and message.content == 'relay' and len(message.attachments) != 0:
            for attachment in message.attachments:
                await attachment.save("/home/pi/Desktop/tasmania_files/"+attachment.filename)
                await message.channel.send("recieved "+str(attachment.filename))