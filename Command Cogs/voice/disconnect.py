import discord, lavalink, re
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"disconnect":{
        "aliases":["disconnect", "leave"],
        "syntax":"",
        "usage":"Disconnects the bot from the voice channel it is in and clears the queue.",
        "category":"voice"
    }})
    @commands.command(name="disconnect", aliases=["leave"])
    async def _disconnect(ctx):

        player = Bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            await ctx.send(embed=discord.Embed(title="Not connected to a voice channel.", colour=general_utils.Colours.red))
            return

        if not await Bot.ensure_voice(ctx):
            return

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "You arent connected to my voice channel!"))
            return

        player.queue.clear()

        await player.stop()

        await ctx.voice_client.disconnect(force=True)

        disconnect_embed = discord.Embed(title="Disconnected and cleared the queue. Have a nice day!", colour=general_utils.Colours.red)
        #disconnect_embed = general_utils.format_embed(ctx.author, disconnect_embed)
        await ctx.send(embed=disconnect_embed)

    Bot.add_command(_disconnect)