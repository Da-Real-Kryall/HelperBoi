import discord, os, asyncio, string, random
from django.utils import timezone
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from utils import general_utils, database_utils

load_dotenv()
stop_event = asyncio.Event()
loop = asyncio.get_event_loop()

Bot = commands.Bot(command_prefix='!kbr ', intents=discord.Intents.all())
Bot.command_info = {}


extension_paths = []

for directory in os.listdir('./Command Cogs'):
    _directory = os.listdir(f"./Command Cogs/{directory}")
    if _directory != []:
        for _file in _directory:
            if _file.endswith(".py"):
                extension_paths += ["Command Cogs."+directory+"."+_file[:-3]]

for extension in extension_paths:
    Bot.load_extension(extension)


categories = {
    "utility":"Utility/Moderation Commands:",
    "fun":"Fun Commands:",
    "voice":"Voice Channel Commands: (W.I.P)",
    "economy":"Economy Commands:",
    "cah":"Cards-Against-Humanity Commands:"
}

Bot.command_info.update({"help":{
    "aliases":["helpeth", "help", "hewp", "<bot ping>"],
    "syntax":"[command]",
    "usage":"Use for help and info with the bot, using the command argument will instead return help about the given command.",
    "category":"utility"
}})


Bot.remove_command('help')

@Bot.command(name="help", aliases=["helpeth", "hewp"])
async def _help(ctx, command=None):
    #general help, like that returned by the ping
    if command == None:
        help_embed = discord.Embed(title=f"**{Bot.user.display_name}'s Commands & Info**", colour=general_utils.Colours.main, description=f"The command prefix is `{Bot.command_prefix}`, so `{Bot.command_prefix}command` is generally how commands are used. Also use `{Bot.command_prefix}help [command]` for info on its usage.", timestamp=datetime.now(timezone.utc))
        
        help_embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        for category in categories:
            commandlist = []
            for command in list(Bot.commands):
                if Bot.command_info[command.name]["category"] == category:
                    commandlist += [command]
            if commandlist != []:
                help_embed.add_field(name=categories[category], value='`'+('`, `'.join([str(command) for command in commandlist]))+'`', inline=True)

        #consider adding cube mcdude advert
        help_embed.add_field(name="Notes:", inline=False, value=f"Use `{Bot.command_prefix}botinfo` for information about this bot, and `{Bot.command_prefix}privacy` for info regarding the info that is saved and used by {Bot.user.display_name}.")
    
    elif command != None:

        #save command name for use later, in case it was an alias
        command_name_given = str(command)
        
        command = Bot.get_command(command)

        #check if command doesnt exist
        if command == None: 
            await ctx.send(embed=discord.Embed(title="Hey!", description="Thats not an exiting command! please try something else.", colour=general_utils.Colours.main, timestamp=datetime.now(timezone.utc)))
        elif command != None:
            help_embed = discord.Embed(title=f"**Info For The Command: \"{command.name}\"**")
            help_embed = general_utils.format_embed(ctx.author, help_embed)
            
            help_embed.add_field(name="Syntax:", value=f"{Bot.command_prefix}{command} {Bot.command_info[command.name]['syntax']}")

            aliases = list(command.aliases)+[command.name]
            aliases.remove(command_name_given)

            if len(aliases) == 0:
                aliases = ['None']

            help_embed.add_field(name="Aliases:", value=', '.join(aliases))

            help_embed.add_field(name="Usage:", value=Bot.command_info[command.name]["usage"], inline=False)

            

    await ctx.send(embed=help_embed)

"""
Bot.command_info.update({"test":{
    "aliases":[],
    "syntax":"",
    "usage":"Just a debug command, sends \"test\".",
    "category":"utility"
}})
@Bot.command(name="test")
async def _test(ctx):
    await ctx.send('test')
"""

@Bot.event
async def on_message(message):
    if Bot.user in message.mentions and len(message.content.split(" ")) == 1:

        help_embed = discord.Embed(title=f"**{Bot.user.display_name}'s Commands & Info**", description=f"The command prefix is `{Bot.command_prefix}`, so `{Bot.command_prefix}command` is generally how commands are used. Also use `{Bot.command_prefix}help [command]` for info on its usage.")
        
        help_embed = general_utils.format_embed(message.author, help_embed)
        for category in categories:
            commandlist = []
            for command in list(Bot.commands):
                if Bot.command_info[command.name]["category"] == category:
                    commandlist += [command]
            if commandlist != []:
                help_embed.add_field(name=categories[category], value='`'+('`, `'.join([str(command) for command in commandlist]))+'`', inline=True)
        
        #consider adding cube mcdude advert
        help_embed.add_field(name="Notes:", inline=False, value=f"Use `{Bot.command_prefix}botinfo` for information about this bot, and `{Bot.command_prefix}privacy` for info regarding the info that is saved and used by {Bot.user.display_name}.")

        await message.channel.send(embed=help_embed)
   
    await Bot.process_commands(message)      

@Bot.event
async def on_command_error(ctx, error):
    if error.__class__ == commands.errors.NoPrivateMessage:
        await ctx.send(embed=general_utils.error_embed(True, "This command can only be used in servers!"))
    else:
        await ctx.send(embed=general_utils.error_embed(True, f"{error}\n\nUse `{Bot.command_prefix}report_bug <bug>` if you want to report this as an unfixed issue."))

@Bot.event
async def on_connect():
    print("I'm ready!")
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {str(len(Bot.guilds))} server{'s' if len(Bot.guilds) > 1 else ''} | @{str(Bot.user.name)} for help."))

with open(os.getcwd()+"/token.txt") as nonofile:
    nonokey = nonofile.read()

database_utils.init_main()

Bot.run(nonokey)

#windows xp statrup noise