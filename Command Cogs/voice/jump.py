import discord, time
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"jump":{
        "aliases":["jump", "seek"],
        "syntax":"<num seconds>",
        "usage":"Jumps to the given position in the current song, given in seconds. if a plus or minus is placed before the number of seconds the place to jump to will become relative. (e.g. +10 will jump forward 10 seconds)",
        "category":"voice"
    }})
    @commands.command(name="jump", aliases=["seek"])
    async def _jump(ctx, num_seconds):
        if general_utils.represents_int(num_seconds) == False:
            await ctx.send(embed=general_utils.error_embed(True, "You must provide a valid integer for the number of seconds to jump, optionally prefixxed by + or - for relative jump positions."))
            return
        is_relative = False
        if num_seconds[0] in ['+', '-']:
            is_relative = True
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        if is_relative:
            #print(player.position_timestamp/1000, player.position)
            destination = player.position+int(num_seconds)*1000
        else:
            destination = int(num_seconds)*1000
        if not player.is_connected:
            await ctx.send(embed=discord.Embed(title="Not connected to a voice channel.", colour=general_utils.Colours.red))
            return
        jump_embed = discord.Embed(colour=general_utils.Colours.red)
        if player.current != None:
            if destination > player.current.duration:
                await ctx.send(embed=general_utils.error_embed(True, "That is more seconds than is in the current track, use the `skip` command to skip songs if that was your intention."))
                return
            jump_embed.title = f"Jumped {'back' if player.position > destination else 'forwards'} to {general_utils.strf_timedelta(int(destination/1000)) if destination > 0 else 'to the start'}" #, song duration is {general_utils.strf_timedelta(int(player.current.duration/1000))}
            await player.seek(destination)
        else:
            jump_embed.title = "There isnt a song playing."
        await ctx.send(embed=jump_embed)

    Bot.add_command(_jump)