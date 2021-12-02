import discord, tempfile, time, os
from gtts import gTTS
from discord.ext import commands

def setup(Bot):
    Bot.current_nm_sessions = { #server id: []]
        0: { #example
            "voice_client": None, #vc object
            "users": {
                0: "tld0", #user id: accent/top level domain in use
                1: "tld1"
            }
        }
    }
    @Bot.listen()
    async def on_message(message):
        if message.content[:len(await Bot.get_prefix(message))] == await Bot.get_prefix(message) or len(message.content) > 500:
            return
        if hasattr(message.channel, "me"):
            return
        if message.guild.id in Bot.current_nm_sessions:
            if message.author.id in Bot.current_nm_sessions[message.guild.id]["users"]:

                vc = Bot.current_nm_sessions[message.guild.id]["voice_client"]
                tts = gTTS(text = message.content, tld=Bot.current_nm_sessions[message.guild.id]["users"][message.author.id])

                tmp_file=tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp_file.name)
                tmp_file.close()

                vc.play(discord.FFmpegPCMAudio(tmp_file.name))
                time.sleep(0.4)
                os.unlink(tmp_file.name)

