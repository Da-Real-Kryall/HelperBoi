import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"volume":{
        "aliases":["volume", "set_volume"],
        "syntax":"[new volume]",
        "usage":"Returns the current volume or sets the new volume to the one given. If a + or - goes before the given volume the new value will be the current volume plus the given one. (e.g -10 will decrease volume by 10%)",
        "category":"voice"
    }})
    @commands.command(name="volume", aliases=["set_volume"])
    async def _volume(ctx, volume=None):
        if not await Bot.ensure_voice(ctx):
            return
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        if volume == None:
            await ctx.send(embed=discord.Embed(title=f"The current volume is {player.volume}%", colour=general_utils.Colours.red))
            return
        elif general_utils.represents_int(volume) == False:
            await ctx.send(general_utils.error_embed(Bot, ctx, False, f"The volume specified is not a valid number"))
            return
        else:
            is_relative = False
            if volume[0] in ['+', '-']:
                is_relative = True
            if is_relative:
                destination = player.volume+int(volume)
            else:
                destination = int(volume)
            volume_embed=discord.Embed(colour=general_utils.Colours.red)
            if destination > 1000:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Please spare our eardrums, the volume is capped at a rather generous 1000%."))
                return
            if destination == player.volume:
                volume_embed.title = f"Volume wasn't changed, it is already {destination}%."
            else:
                volume_embed.title = f"Volume {'decreased' if player.volume > destination else 'increased'} to {destination}%."
            await player.set_volume(destination)
            await ctx.send(embed=volume_embed)
    Bot.add_command(_volume)