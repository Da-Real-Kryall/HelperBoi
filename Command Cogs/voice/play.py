import discord, lavalink, re
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"play":{
        "aliases":["play"],
        "syntax":"<song>",
        "usage":"Used after the bot has joined a voice channel in the current server, will play a song determined by the query or add it to the queue if a song is already playing.",
        "category":"voice"
    }})
    @commands.command(name="play")
    async def _play(ctx, *, query: str):

        if not await Bot.ensure_voice(ctx):
            return

        player = Bot.lavalink.player_manager.get(ctx.guild.id)

        # SoundCloud searching is possible by prefixing "scsearch:" instead
        if not re.compile(r'https?://(?:www\.)?.+').match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            await ctx.send(embed=general_utils.error_embed(True, "No songs were found!"))
            return
        track = results['tracks'][0]
        embed_title = 'Song added to queue:'
        embed_desc = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
        
        embed_thumbnail = f"https://img.youtube.com/vi/{track['info']['identifier']}/default.jpg"

        track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
        player.add(requester=ctx.author.id, track=track)
        embed_desc += f'\n\nDuration is {general_utils.strf_timedelta(int(track.duration/1000))}.'
        playing_embed = general_utils.format_embed(ctx.author, discord.Embed(title=embed_title, description=embed_desc), "red")
        playing_embed.set_thumbnail(url=embed_thumbnail)
        await ctx.send(embed=playing_embed)

        if not player.is_playing:
            await player.play()

    Bot.add_command(_play)