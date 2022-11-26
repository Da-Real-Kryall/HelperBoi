import discord
from datetime import datetime
from django.utils import timezone
from discord import app_commands
from discord.ext import commands
from utils import general_utils

class MoveMessages(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MoveMessages cog is ready.")

    #make the description of a bool delete argument that says "Whether or not to delete the messages after moving them."
    @app_commands.command(name="movemessages", description="Moves messages from one channel to another.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(delete="Whether or not to delete the messages after moving them.")
    async def _movemessages(self, interaction: discord.Interaction, destination: discord.TextChannel, amount: app_commands.Range[int, 1, 100], delete: bool = False, source: discord.TextChannel = None):
        await interaction.response.defer(ephemeral=True)
        if source is None:
            source = interaction.channel
        message_list = []

        async for message in source.history(limit=amount):
            msg_to_append = []
            # if message was a reply or from a slash command, append the message content
            msg_content = ""
            if message.reference is not None:
                content = message.reference.resolved.content.replace("`", "\\`")
                msg_content += f"> @{message.reference.resolved.author.name}#{message.reference.resolved.author.discriminator}{':' if len(content) != 0 else ''} {content[:30]}{'...' if len(content) > 30 else ''}\n"
            elif type(message.interaction) == discord.message.MessageInteraction:
                msg_content += f"**┎╴**@{message.interaction.user.name}#{message.interaction.user.discriminator} used /{message.interaction.name}\n"
            msg_content += message.content

            msg_to_append += [msg_content]
                
            files = []
            for attachment in message.attachments:
                file = await attachment.to_file()
                files += [file]
            msg_to_append += [files] #1
            
            embeds = []
            for embed in message.embeds:
                embeds += [embed]
            msg_to_append += [embeds] #2

            msg_to_append += [message.author] #3
            #if message.reference is not None or type(message.interaction) == discord.message.MessageInteraction:
            #    x += 1
            #else:
            #    x = 0
            #msg_to_append[3] += "\u200b"*x
            message_list += [msg_to_append]
        
        if delete:
            await interaction.channel.purge(limit=amount)

        for message in reversed(message_list):
            try:
                await general_utils.send_via_webhook(channel=destination, Bot=self.Bot, message=message[0], username=message[3].name, avatar_url=message[3].avatar.url, files=message[1], embeds=message[2])
            except discord.errors.HTTPException:
                pass
        await interaction.followup.send(embed=general_utils.Embed(author=interaction.user, title=f"Moved {amount} messages from **#{source.name}** to **#{destination.name}**."), ephemeral=False)

async def setup(Bot):
    await Bot.add_cog(MoveMessages(Bot))


#    Bot.command_info.update({"movemessages":{
#        "aliases":["movemessages", "mmsg"],
#        "syntax":"<destination channel id> <num messages>",
#        "usage":"Moves the given number of messages from the current channel to the channel with the id given in the same server.",
#        "category":"utility"
#    }})
#    @commands.has_permissions(manage_messages=True)
#    @commands.command(name="movemessages", aliases=["mmsg"])
#    async def _movemessages(ctx, destination, amount):
#        await ctx.message.delete()
#
#        if general_utils.represents_int(amount) == False or int(amount) < 1:
#            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Please give a valid positive integer for message amount."))
#
#        DestinationChannel = ctx.guild.get_channel(int(destination))
#
#        messagelist = []
#        if ctx.guild.get_member(Bot.user.id).guild_permissions.manage_webhooks == False:
#            async for message in ctx.channel.history(limit=int(amount)-1): #send as embeds
#                if message.author.colour == discord.Colour(0x000000): #change colour if none is given
#                    authorcolour = discord.Colour(0xCBCBCB)
#                else:
#                    authorcolour = message.author.colour
#
#                if message.author.bot: #change sent message if the message author was a bot
#                    embedtoappend = discord.Embed(timestamp=datetime.now(timezone.utc), title=message.author.name+'  <:B_:768779404888899605><:O_:768779415852417034><:T_:768779427487416341>                    ', description=message.content, colour=authorcolour)
#                else:
#                    embedtoappend = discord.Embed(timestamp=datetime.now(timezone.utc), title=message.author.name+'                           ', description=message.content, colour=authorcolour)
#
#                if len(message.embeds) >= 1: #idk if it was a webbhook
#                    embedtoappend.set_footer(text='(Message had '+str(len(message.embeds))+' embed, shown below)')
#                if len(message.embeds) != 0:
#                    for embed in message.embeds:
#                        messagelist.append(embed)
#
#                if message.is_system(): #deal with system messages, still need to get a sys_msg_dict
#                    embedtoappend = discord.Embed(title=':wrench: '+message.type.name+'                           ', description=message.system_content, colour=discord.Colour(0x99aab5))
#                    embedtoappend.set_footer(text='Event occured at: '+message.created_at.strftime('%A %d %B %Y'))
#
#                messageforforloop = message #amazing var names
#                if len(message.attachments) != 0:
#                    for attachment in message.attachments:
#                        messagelist.append(discord.Embed(title=messageforforloop.author.name+'                           ', description=attachment.url, colour=authorcolour))
#                        if len(messageforforloop.embeds) >= 1:
#                            embedtoappend.set_footer(text=str(messageforforloop.created_at.strftime('%A %d %B %Y'))+' (Message had '+str(len(messageforforloop.embeds))+' embed, shown below)')
#                        else:
#                            embedtoappend.set_footer(text=str(messageforforloop.created_at.strftime('%A %d %B %Y')))
#                if embedtoappend.description != '':
#                    messagelist.append(embedtoappend)
#
#            for message in reversed(messagelist): #send messages
#                try:
#                    await DestinationChannel.send(embed=message)
#                except:
#                    await DestinationChannel.send(message)
#        else:
#            async with ctx.typing():
#                async for message in ctx.channel.history(limit=int(amount)-1): #send using webhooks
#                    msg_to_append = []
#                    if message.content != '':
#                        msg_to_append += [message.content] #0
#                    else:
#                        msg_to_append += [None] #0
#                        
#                    files = []
#                    for attachment in message.attachments:
#                        file = await attachment.to_file()
#                        files += [file]
#                    msg_to_append += [files] #1
#                    
#                    embeds = []
#                    for embed in message.embeds:
#                        embeds += [embed]
#                    msg_to_append += [embeds] #2
#
#                    msg_to_append += [message.author] #3
#                    
#                    messagelist += [msg_to_append]
#                    
#            for message in reversed(messagelist): #send messages
#                await general_utils.send_via_webhook(DestinationChannel, Bot, message[0], username=message[3].display_name, avatar_url=message[3].avatar.url, files=message[1], embeds=message[2])
#            await DestinationChannel.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Moved {amount} messages from #{ctx.channel.name}.")))
#            await ctx.channel.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Moved {amount} messages to #{DestinationChannel.name}.")))
#
#    Bot.add_command(_movemessages)