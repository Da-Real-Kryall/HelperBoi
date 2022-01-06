import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"queue":{
        "aliases":["shuffle"],
        "syntax":"",
        "usage":"Toggles queue shuffle.",
        "category":"voice"
    }})
    @commands.command(name="queue")
    async def _shuffle(ctx):
        await Bot.ensure_voice(ctx)
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        await player.skip()
        skipped_embed=discord.Embed(colour=general_utils.Colours.red)
        if player.current != None:
            embed_title = f"Current queue:"+("")
            skipped_embed.description = f'[{player.current.title}](https://youtu.be/{player.current.identifier})'
            skipped_embed.set_thumbnail(url=f"https://img.youtube.com/vi/{player.current.identifier}/default.jpg")
        else:
            embed_title = "There are no songs in the queue."
        skipped_embed.title = embed_title
        await ctx.send(embed=skipped_embed)
    Bot.add_command(_shuffle)