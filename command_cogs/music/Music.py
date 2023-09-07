import discord, re, lavalink, random
from discord.ext import commands
from discord import app_commands
from utils import general_utils

class Music(commands.GroupCog, name="music"):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot
        def queue_embed_modifier(embed: discord.Embed, scroll_index: int, interaction: discord.Interaction) -> discord.Embed:
            player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
            queue_embed = embed
            embed_desc = ""

            if player.current != None:
                embed_title = f"Current queue:"+(" :twisted_rightwards_arrows:" if player.shuffle else '')+(" :repeat:" if player.repeat else '')

                offset = 0
                if len(player.queue) > 10:
                    offset = scroll_index - 5
                    if offset < 0:
                        offset = 0
                    if offset > len(player.queue) - 10:
                        offset = len(player.queue) - 10
                
                if offset == 0:
                    embed_desc += f"` {'>' if 0 == scroll_index else ' '} `**1.** [{player.current.title}](https://youtu.be/{player.current.identifier}) **[**Playing**]**\n"
                else:
                    embed_desc += f"[{offset} more]\n"
                for num, song in enumerate(player.queue[offset:offset+10]):
                    num += offset
                    embed_desc += f"` {'>' if num+1 == scroll_index else ' '} `**{num+2}.** [{song.title}](https://youtu.be/{song.identifier}) {'**[**Next**]**' if num == 0 else ''}\n"
                if offset != len(player.queue) - 10:
                    embed_desc += f"[{len(player.queue)-10 - offset} more]"

                queue_embed.description = embed_desc
                embed.set_footer(text=f"Track {scroll_index+1} of {len(player.queue)}")
            else:
                embed_title = "There are no songs in the queue."
            queue_embed.title = embed_title

            return queue_embed
        self.queue_embed_modifier = queue_embed_modifier

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if "custom_id" in interaction.data:
            if interaction.data["custom_id"].startswith("queue."):
                def delete_queue_song(scroll_index: int) -> int:
                    player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
                    if scroll_index == 0:
                        player.skip()
                    else:
                        player.queue.pop(scroll_index-1)
                    return max(scroll_index-1, 0)
                functions = general_utils.make_functions_dict("queue", self.queue_embed_modifier, delete_queue_song)
                await general_utils.interaction_listener_generator("queue", functions)(interaction)
            

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music cog loaded.")
    
    @app_commands.command(name="volume", description="Set the bot's music volume.")
    async def _volume(self, interaction: discord.Interaction, volume: app_commands.Range[int, 0, 1000]=None) -> None:
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)

        volume_embed=general_utils.Embed(author=interaction.user, colour="lime")
        if volume != None:
            if volume == player.volume:
                volume_embed.title = f"Volume wasn't changed, it is already at {volume}%."
            else:
                volume_embed.title = f"Volume {'decreased' if player.volume > volume else 'increased'} to {volume}%."
            if volume == 1000:
                volume_embed.description = "(I wish your eardrums the best of luck.)"
            await player.set_volume(volume)
        else:
            volume_embed.title = f"Volume is currently at {player.volume}%."
            if player.volume == 1000:
                volume_embed.description = "(I wish your eardrums the best of luck.)"

        await interaction.response.send_message(embed=volume_embed, ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="play", description="Queries the given song from YouTube and adds it to the queue. Works for playlist web links!")
    async def _play(self, interaction: discord.Interaction, query: str) -> None:
        await interaction.response.defer()

        if not await self.Bot.ensure_voice(interaction):
            return

        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)

        # SoundCloud searching is possible by prefixing "scsearch:" instead
        query = query.strip('<>')
        if not re.compile(r'https?://(?:www\.)?.+').match(query):
            query = f'ytsearch:{query} song'

        results = await player.node.get_tracks(query)

        if not results or not results.tracks:
            await interaction.followup.send(embed=general_utils.error_embed(author=interaction.user, message="No songs were found!", apologise=True), ephemeral=general_utils.is_ghost(interaction.user.id))
            return

        if results.load_type == 'PLAYLIST_LOADED':
            tracks = results.tracks
            for track in tracks:
                player.add(requester=interaction.user.id, track=track)
    
            embed_title = f'{len(tracks)} songs added to queue:'
            embed_desc = '\n'.join([f'**{index}.** [{track["info"]["title"]}]({track["info"]["uri"]})' for index, track in enumerate(tracks, start=1)])
            embed_desc += f'\n\nDuration: {general_utils.strf_timedelta(int(sum([track.duration for track in tracks])/1000))}.'
            embed_thumbnail = f"https://img.youtube.com/vi/{tracks[0]['info']['identifier']}/default.jpg"
            
        else:
            track = results['tracks'][0]

            track = lavalink.models.AudioTrack(track, interaction.user.id, recommended=True)
            player.add(requester=interaction.user.id, track=track)

            embed_title = 'Song added to queue:'
            embed_desc = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed_desc += f'\n\nDuration: {general_utils.strf_timedelta(int(track.duration/1000))}.'
            embed_thumbnail = f"https://img.youtube.com/vi/{track['info']['identifier']}/default.jpg"

        while len(embed_desc) > 4090:
            embed_desc = '\n'.join(embed_desc.split('\n')[:-2])+'\n...'
            
        playing_embed = general_utils.Embed(author=interaction.user, title=embed_title, description=embed_desc, colour="lime")
        playing_embed.set_thumbnail(url=embed_thumbnail)

        await interaction.followup.send(embed=playing_embed, ephemeral=general_utils.is_ghost(interaction.user.id))

        if not player.is_playing:
            await player.play()

    @app_commands.command(name="queue", description="Show the current queue.")
    async def _queue(self, interaction: discord.Interaction) -> None:
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)

        queue_embed = self.queue_embed_modifier(general_utils.Embed(colour="lime"), 0, interaction)
        await interaction.response.send_message(embed=queue_embed, view=(general_utils.Controller("queue", 0, len(player.queue)+1) if player.current != None else None), ephemeral=general_utils.is_ghost(interaction.user.id))
        
    @app_commands.command(name="shuffle", description="Toggle queue shuffle.")
    async def _shuffle(self, interaction: discord.Interaction) -> None:
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        player.set_shuffle(not player.shuffle)
        if player.shuffle:
            embed_title = f"Enabled shuffle."
        else:
            embed_title = f"Disabled shuffle."
        shuffle_embed = general_utils.Embed(author=interaction.user, title=embed_title, colour="lime")
        await interaction.response.send_message(embed=shuffle_embed, ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="skip", description="Skip the current song.")
    async def _skip(self, interaction: discord.Interaction) -> None:
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        if not player.current:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="There is nothing playing right now.", apologise=False), ephemeral=True)
        await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=f"Skipped {player.current.title}.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))
        await player.skip()

    @app_commands.command(name="pause", description="Pauses the current song.")
    async def _pause(self, interaction: discord.Interaction):
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        if player.paused == False:
            await player.set_pause(True)
            await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=":pause_button:  Pausing music.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))
        else:
            await player.set_pause(False)
            await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=":arrow_forward:  Resuming music.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))
    
    @app_commands.command(name="resume", description="Resumes the current song.")
    async def _resume(self, interaction: discord.Interaction):
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        if player.paused == False:
            await player.set_pause(True)
            await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=":pause_button:  Pausing music.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))
        else:
            await player.set_pause(False)
            await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=":arrow_forward:  Resuming music.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="no_mic", description="Toggles relaying any messages you send from the current text channel into your current vc.")
    async def _no_mic(self, interaction: discord.Interaction):

        tld_list = [
            "com.au",
            "co.uk",
            "com",
            "ca",
            "co.in",
            "ie",
            "co.za",
            "fr",
            "com.br",
            "pt",
            "com.mx",
            "es"
        ]

        author = interaction.guild.get_member(interaction.user.id)
        
        if interaction.guild.id not in self.Bot.current_nm_sessions:
            channel = author.voice.channel
            vc = await channel.connect()

            self.Bot.current_nm_sessions.update({
                int(interaction.guild.id): {
                    "voice_client": vc,
                    "users": {
                        int(author.id): random.choice(tld_list)
                    }
                }
            })
            await interaction.response.send_message(embed=general_utils.Embed(author=author, title="You have been added to the session.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))
        else:
            if author.id not in self.Bot.current_nm_sessions[interaction.guild.id]["users"]:
                self.Bot.current_nm_sessions[interaction.guild.id]["users"].update({
                    int(author.id): random.choice(tld_list)
                })
            else:
                self.Bot.current_nm_sessions[interaction.guild.id]["users"].pop(author.id)
                await interaction.response.send_message(embed=general_utils.Embed(author=author, title="You have been removed from the session.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))
                if len(self.Bot.current_nm_sessions[interaction.guild.id]["users"]) == 0:
                    await self.Bot.current_nm_sessions[interaction.guild.id]["voice_client"].disconnect()
                    self.Bot.current_nm_sessions.pop(interaction.guild.id)
                    await interaction.response.send_message(embed=general_utils.Embed(author=author, title="Ended the session in this channel because there were no active users. Have a nice day!", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="loop", description="Toggles looping of the song queue.")
    async def _loop(self, interaction: discord.Interaction):
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        player.set_repeat(not player.repeat)
        if player.repeat:
            embed_title = f"Enabled looping."
        else:
            embed_title = f"Disabled looping."
        repeat_embed = general_utils.Embed(author=interaction.user, title=embed_title, colour="lime")
        await interaction.response.send_message(embed=repeat_embed, ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="seek", description="Seeks to a specific point in the current song.")
    async def _seek(self, interaction: discord.Interaction, seconds: int):
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        if not player.current:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="There is nothing playing right now!", apologise=False), ephemeral=True)
        if seconds > player.current.duration:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="You cannot seek to a point in the song that is longer than the song itself.", apologise=False), ephemeral=True)
        await player.seek(seconds * 1000)
        await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=f"Seeked to {seconds} seconds.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="leave", description="Leaves the current voice channel. (And clears the queue.)")
    async def _leave(self, interaction: discord.Interaction):

        bot_member = interaction.guild.get_member(self.Bot.user.id)
        if bot_member.voice == None:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="I am not in a voice channel!", apologise=False), ephemeral=True)

        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)

        player.queue.clear()
        await player.stop()
        await interaction.guild.voice_client.disconnect(force=False)

        disconnect_embed = general_utils.Embed(author=interaction.user, title="Disconnected and cleared the queue. Have a nice day!", colour="lime")
        await interaction.response.send_message(embed=disconnect_embed, ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="join", description="Joins the voice channel you are in.")
    async def _join(self, interaction: discord.Interaction):
        # check if i'm already in a voice channel

        bot_member = interaction.guild.get_member(self.Bot.user.id)
        if bot_member.voice != None:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="I am already in a voice channel!", apologise=False), ephemeral=True)
        if not await self.Bot.ensure_voice(interaction):
            #await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="I'm already in a voice channel", apologise=False), ephemeral=True)
            return
        author = interaction.guild.get_member(interaction.user.id)
        channel = author.voice.channel
        await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=f"Joined {channel.name}.", colour="lime"), ephemeral=general_utils.is_ghost(interaction.user.id))

    @app_commands.command(name="current", description="Shows info about the current song.")
    async def _current(self, interaction: discord.Interaction):
        if not await self.Bot.ensure_voice(interaction):
            return
        player = self.Bot.lavalink.player_manager.get(interaction.guild.id)
        if not player.current:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="There is nothing playing right now!", apologise=False), ephemeral=True)
        song = player.current
        embed = general_utils.Embed(author=interaction.user, title=f"Currently playing {song.title} by {song.author}.", colour="lime")
        embed.add_field(name="Duration:", value=f"{general_utils.strf_timedelta(int(song.duration/1000))}")
        embed.add_field(name="Position:", value=f"{general_utils.strf_timedelta(int(player.position/1000))}")
        embed.add_field(name="Requested by:", value=f"{interaction.guild.get_member(song.requester).mention}")
        embed.set_thumbnail(url=f"https://img.youtube.com/vi/{song.identifier}/default.jpg")
        await interaction.response.send_message(embed=embed, ephemeral=general_utils.is_ghost(interaction.user.id))
        
async def setup(Bot):
    await Bot.add_cog(Music(Bot))