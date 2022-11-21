import discord, os, sys, asyncio
from discord.ext import commands
from utils import general_utils
from discord import app_commands
from typing import Union

def get_help_embed(Bot, author: discord.User) -> discord.Embed:

    embed = general_utils.Embed(author=author, title="HelperBoi's Commands & Info")

    embed.description = """:wave: *Hello!* My end goal and purpose is to simply help in any way I possibly can; be it with moderation, entertainment, or general utility.\n\n__**My main features are:**__\n • A fully fledged music player.\n • A dynamic Cards-Against-Humanities system.\n • Toggleable light, unobtrusive swear filtering.\n • A complete economy system with inventories, money and gambling!\n • Dad jokes!\n • "And much, much more!"\n\u200b"""

    commands = Bot.tree.get_commands()

    categories = {}
    
    for command in commands:
        if type(command) == discord.app_commands.Command:
            category = command.module.split(".")[-2]
            if category not in categories:
                categories.update({category: [command.name]})
            else:
                categories[category].append(command.name)

        if type(command) == discord.app_commands.Group:
            for subcommand in command.commands:
                category = subcommand.module.split(".")[-2]
                if category not in categories:
                    categories.update({category: [command.name+' '+subcommand.name]})
                else:
                    categories[category].append(command.name+' '+subcommand.name)

    for category, commands in categories.items():
        embed.add_field(name=category.capitalize()+":", value="`"+'`, `'.join(commands)+"`")

    embed.add_field(name="Notes:", value="To use commands, type `/` followed by the command name in question; The rest should be intuitive enough.\n\nAlso, if you have any suggestions, feel free to send them to my owner (Kryal|#2231) with the `suggest` command!")#. If you need help with a specific command, type `/help <command>`.
    
    return embed

class Help(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog Loaded")
    
    @app_commands.command(name="help", description="Shows a command list and some bot info, or shows info about a specific command.")
    async def _help(self, interaction: Union[discord.Interaction, discord.User]) -> None:
        embed = get_help_embed(self.Bot, interaction.user)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # run help command on bot mention
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.Bot.user in message.mentions:
            msg = await message.reply(embed=get_help_embed(self.Bot, message.author))
            await msg.add_reaction("💥")

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '💥' and reaction.message.id == msg.id
            try:
                reaction, user = await self.Bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                return
            else:
                await msg.delete()
async def setup(Bot):
    await Bot.add_cog(Help(Bot))