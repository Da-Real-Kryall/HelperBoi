import discord, lavalink
from discord.ext import commands
from utils import general_utils

def setup(Bot): #this was taken straight from the lavalink quickstart, the site said this is the preferred way to do things.

    
    #Bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'eu', 'default-node')  # Host, Port, Password, Region, Name
    async def track_hook(event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = Bot.get_guild(guild_id)
            channel = guild.get_channel(Bot.lavalink.player_manager.get(guild_id).fetch("text_channel"))
            await channel.send(embed=discord.Embed(title=f"No more songs in the queue, ending the session.", colour=general_utils.Colours.red))
            #print(dir(event))
            #print(event)
            await guild.voice_client.disconnect(force=True)
        if isinstance(event, lavalink.events.TrackStartEvent):
            guild_id = int(event.player.guild_id)
            guild = Bot.get_guild(guild_id)
            channel = guild.get_channel(Bot.lavalink.player_manager.get(guild_id).fetch("text_channel"))
            embed_desc = f"[{event.player.current.title}](https://youtu.be/{event.player.current.identifier})"#\n\nDuration is {general_utils.strf_timedelta(int(event.player.current.duration/1000))}."
            trackstart_embed = discord.Embed(title=f"Now playing:", description=embed_desc, colour=general_utils.Colours.red)
            trackstart_embed.set_thumbnail(url=f"https://img.youtube.com/vi/{event.player.current.identifier}/default.jpg")
            await channel.send(embed=trackstart_embed)
    lavalink.add_event_hook(track_hook)

    class LavalinkVoiceClient(discord.VoiceClient):
        def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
            self.client = client
            self.channel = channel
            # make sure there exists a client already
            if hasattr(self.client, 'lavalink'):
                self.lavalink = self.client.lavalink
            else:
                self.client.lavalink = lavalink.Client(client.user.id)
                self.client.lavalink.add_node(
                        'localhost',
                        2333,
                        'youshallnotpass',
                        'au',
                        'default-node')
                self.lavalink = self.client.lavalink

        async def on_voice_server_update(self, data):
            # the data needs to be transformed before being handed down to
            # voice_update_handler
            lavalink_data = {
                    't': 'VOICE_SERVER_UPDATE',
                    'd': data
                    }
            await self.lavalink.voice_update_handler(lavalink_data)

        async def on_voice_state_update(self, data):
            # the data needs to be transformed before being handed down to
            # voice_update_handler
            lavalink_data = {
                    't': 'VOICE_STATE_UPDATE',
                    'd': data
                    }
            await self.lavalink.voice_update_handler(lavalink_data)

        async def connect(self, *, timeout: float, reconnect: bool) -> None: #if stuff doesnt work in edge cases this is probably the culprit
            #player = self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
            #player.store("text_channel", self.channel.id)
            print(self, dict(locals()), "e")
            await self.channel.guild.change_voice_state(channel=self.channel, self_deaf=True)

        async def disconnect(self, *, force: bool) -> None:
            player = self.lavalink.player_manager.get(self.channel.guild.id)
            if not force and not player.is_connected:
                return
            await self.channel.guild.change_voice_state(channel=None)
            player.channel_id = None
            self.cleanup()

    async def _ensure_voice(ctx):
        player = Bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        player.store("text_channel", ctx.channel.id)
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send(embed=general_utils.error_embed(False, 'Please join a voicechannel first.'))
            return False
        if not player.is_connected:
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:  # Check user limit too?
                await ctx.send(embed=general_utils.error_embed(False, 'I\'m missing the `connect` and `speak` permissions required to play songs...'))
                return False
            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                await ctx.send(embed=general_utils.error_embed(False, 'You need to be in my voicechannel to do this command.'))
                return False
        return True
    Bot.ensure_voice = _ensure_voice