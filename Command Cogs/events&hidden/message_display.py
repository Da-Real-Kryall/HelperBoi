import discord, time
from discord.ext import commands

def setup(Bot):

    printtime = time.strftime('%I:%M %p').lower()
    printdate = time.strftime('%a %d %b')
    Bot._timestamps = [printtime, printdate]

    @Bot.listen()
    async def on_message(message):

        ctntstr = []
        if len(message.embeds) != 0:
            ctntstr += ['embed']
        if len(message.attachments) != 0:
            ctntstr += ['attachment']
        if message.content != '':
            ctntstr += ['"'+message.content+'"']
        ctntstr = ', '.join(ctntstr)
        nowtime = time.strftime('%I:%M %p').lower()
        nowdate = time.strftime('%a %d %b')
        if nowtime != Bot._timestamps[0]:
            Bot._timestamps[0] = time.strftime('%I:%M %p').lower()
            print(f"\n   {time.strftime('%I:%M %p').lower()}")
        if nowdate != Bot._timestamps[1]:
            Bot._timestamps[1] = time.strftime('%a %d %b')
            print(f"\n{time.strftime('%a %d %b')}:")
        if (isinstance(message.channel, discord.channel.DMChannel)) == False:
            print(f"     {message.guild.name}: {' '*(20-len(message.guild.name))} #{message.channel.name}: {' '*(15-len(message.channel.name)+1)} @{message.author.display_name}:{' '*(16-len(message.author.display_name)+2)}{ctntstr}")
        else:
            print(f"(DM) @{message.author.display_name}:{' '*(16-len(message.author.display_name)+2)}{ctntstr}")