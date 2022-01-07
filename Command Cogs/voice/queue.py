import discord
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"queue":{
        "aliases":["shuffle"],
        "syntax":"",
        "usage":"Shows the current song queue",
        "category":"voice"
    }})
    @commands.command(name="queue")
    async def _shuffle(ctx):
        if not await Bot.ensure_voice(ctx):
            return
        player = Bot.lavalink.player_manager.get(ctx.guild.id)
        queue_embed=discord.Embed(colour=general_utils.Colours.red)
        embed_desc = []
        if player.current != None:
            embed_title = f"Current queue:"+(" :twisted_rightwards_arrows:" if player.shuffle else '')+(" :repeat:" if player.repeat else '')
            embed_desc += [f'1. [{player.current.title}](https://youtu.be/{player.current.identifier}) (current)']
            for num, song in enumerate(player.queue):
                embed_desc += [f'{num+2}. [{song.title}](https://youtu.be/{song.identifier})']
            embed_desc = '\n'.join(embed_desc)
            queue_embed.description = embed_desc
        else:
            embed_title = "There are no songs in the queue."
        queue_embed.title = embed_title
        await ctx.send(embed=queue_embed)
    Bot.add_command(_shuffle)