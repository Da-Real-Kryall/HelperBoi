import discord, os
from discord.ext import commands
from utils import general_utils


def setup(Bot):

    Bot.command_info.update({"reload_command":{
        "aliases":["reload_command", "reload"],
        "syntax":"<command>",
        "usage":"Reloads the given command. Only for the bot owner!",
        "category":"utility"
    }})


    @commands.is_owner()
    @commands.command(name="reload_command", aliases=["reload"])
    async def _reload_command(ctx, command=None):

        command_dict = {}
        given_command_string = str(command)

        for directory in os.listdir('./Command Cogs'):
            _directory = os.listdir(f"./Command Cogs/{directory}")
            if _directory != []:
                for _file in _directory:
                    if _file.endswith(".py"):
                        command_dict.update({_file[:-3]:"Command Cogs."+directory+"."+_file[:-3]})
        try:
            command = Bot.get_command(command)
        except:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, 'Please specify a command to reload'))
            return

        if command == None:
            #reload as extension
            if given_command_string in list(command_dict.keys()):
                try:
                    Bot.reload_extension(command_dict[str(given_command_string)])
                    await ctx.send(embed=discord.Embed(title=f"Successfully Reloaded the \"{given_command_string}\" extension.", colour=discord.Colour(0x09df17)))
                except:
                    await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, 'It seems there was an error when reloading the command/extension.'))
            else:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, 'That doesnt seem to be an existing command or extension!'))
        
        elif command != None:
            try:
                Bot.reload_extension(command_dict[str(command)])
                await ctx.send(embed=discord.Embed(title=f"Successfully Reloaded the \"{command}\" command.", colour=general_utils.Colours.green))
            except Exception as e:
                error_embed = discord.Embed(title=f"**{e.__class__.__name__} while reloading the {command} command:**", description=f"```py\n{e.args[0] if hasattr(e, 'msg') == True else str(e)}```", colour=0xea1510)
                if hasattr(e, 'lineno'): 
                    error_embed.set_footer(text=', '.join([(f"{e.filename}" if hasattr(e, 'filename') == True else ""),(f"Line {e.lineno}" if hasattr(e, 'lineno') == True else "")]))
                
                await ctx.send(embed=error_embed)

        #await ctx.send(json.dumps(command_dict, indent=4))

    Bot.add_command(_reload_command)