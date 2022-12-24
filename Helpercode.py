import discord, os, asyncio, lavalink
from dotenv import load_dotenv
from discord.ext import commands
from utils import general_utils, database_utils

database_utils.init_everything()
#database_utils.transfer_all_data()

load_dotenv()
stop_event = asyncio.Event()
loop = asyncio.get_event_loop()

Bot = commands.Bot(command_prefix="!kbr ", intents=discord.Intents.all())
Bot.remove_command("help")

Bot.loop = loop
@Bot.event
async def on_connect(): 

    for directory in os.listdir('./command_cogs'):
        if directory.endswith(".py"):
            await Bot.load_extension("command_cogs."+directory[:-3])
        else:
            for _directory in os.listdir(f"./command_cogs/{directory}"):
                if _directory.endswith(".py"):
                    await Bot.load_extension("command_cogs."+directory+"."+_directory[:-3])

    #lavalink thing
    Bot.lavalink = lavalink.Client(Bot.user.id)
    Bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'au', 'default-node')
    # ansi escape code for green: 
    print("\x1b[32m I'm ready!\x1b[0m")
    #await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {str(len(Bot.guilds))} servers | @{str(Bot.user.name)} for help."))
    while 1:
        await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {str(len(Bot.guilds))} servers | @{str(Bot.user.name)} for help."))
        await asyncio.sleep(60)
    #    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"REWRITE COMPLETED!"))
    #    await asyncio.sleep(15)

@Bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    try:
        await interaction.response.send_message(embed=general_utils.error_embed(message=f"The following error occurred while processing your command:\n```py\n{error}\n```"), ephemeral=True)
    except discord.errors.InteractionResponded:
        await interaction.followup.send(embed=general_utils.error_embed(message=f"The following error occurred while processing your command:\n```py\n{error}\n```"), ephemeral=True)
with open(os.getcwd()+"/tokens.txt") as nonofile:
    nonokey = nonofile.readlines()[0].split(" # ")[0]

Bot.run(nonokey)

#windows xp statrup noise
