import discord
from datetime import datetime
from django.utils import timezone
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"movemessages":{
        "aliases":["movemessages", "mmsg"],
        "syntax":"<destination channel id> <num messages>",
        "usage":"Moves the given number of messages from the current channel to the channel with the id given in the same server.",
        "category":"utility"
    }})
    @commands.has_permissions(manage_messages=True)
    @commands.command(name="movemessages", aliases=["mmsg"])
    async def _movemessages(ctx, destination, amount):
        await ctx.message.delete()

        if general_utils.represents_int(amount) == False or int(amount) < 1:
            await ctx.send(embed=general_utils.error_embed(False, "Please give a valid positive integer for message amount."))

        DestinationChannel = ctx.guild.get_channel(int(destination))
        messagelist = []

        async for message in ctx.channel.history(limit=int(amount)-1):

            if message.author.colour == discord.Colour(0x000000): #change colour if none is given
                authorcolour = discord.Colour(0xCBCBCB)
            else:
                authorcolour = message.author.colour

            if message.author.bot: #change sent message if the message author was a bot
                embedtoappend = discord.Embed(timestamp=datetime.now(timezone.utc), title=message.author.name+'  <:B_:768779404888899605><:O_:768779415852417034><:T_:768779427487416341>                    ', description=message.content, colour=authorcolour)
            else:
                embedtoappend = discord.Embed(timestamp=datetime.now(timezone.utc), title=message.author.name+'                           ', description=message.content, colour=authorcolour)
            
            if len(message.embeds) >= 1: #idk if it was a webbhook
                embedtoappend.set_footer(text='(Message had '+str(len(message.embeds))+' embed, shown below)')
            if len(message.embeds) != 0:
                for embed in message.embeds:
                    messagelist.append(embed)
            
            if message.is_system(): #deal with system messages, still need to get a sys_msg_dict
                embedtoappend = discord.Embed(title=':wrench: '+message.type.name+'                           ', description=message.system_content, colour=discord.Colour(0x99aab5))
                embedtoappend.set_footer(text='Event occured at: '+message.created_at.strftime('%A %d %B %Y'))
            
            messageforforloop = message #amazing var names
            if len(message.attachments) != 0:
                for attachment in message.attachments:
                    messagelist.append(discord.Embed(title=messageforforloop.author.name+'                           ', description=attachment.url, colour=authorcolour))
                    if len(messageforforloop.embeds) >= 1:
                        embedtoappend.set_footer(text=str(messageforforloop.created_at.strftime('%A %d %B %Y'))+' (Message had '+str(len(messageforforloop.embeds))+' embed, shown below)')
                    else:
                        embedtoappend.set_footer(text=str(messageforforloop.created_at.strftime('%A %d %B %Y')))
            if embedtoappend.description != '':
                messagelist.append(embedtoappend)

        for message in reversed(messagelist): #send messages
            try:
                await DestinationChannel.send(embed=message)
            except:
                await DestinationChannel.send(message)
    
    Bot.add_command(_movemessages)