import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"skip":{
        "aliases":["skip"],
        "syntax":"",
        "usage":"Skips the current song.",
        "category":"voice"
    }})
    @commands.command(name="skip")
    async def _skip(ctx):
        if not await Bot.ensure_voice(ctx):
            return
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        skipped_embed=discord.Embed(colour=general_utils.Colours.red)
        await player.skip()
        if player.current != None:
            skipped_embed.title = f"Skipped the current song, now playing:"
            skipped_embed.description = f"[{player.current.title}](https://youtu.be/{player.current.identifier})\n\nDuration is {general_utils.strf_timedelta(int(player.current.duration/1000))}."
            skipped_embed.set_thumbnail(url=f"https://img.youtube.com/vi/{player.current.identifier}/default.jpg")
            await ctx.send(embed=skipped_embed)
    Bot.add_command(_skip)