import discord, random, os, tempfile
from discord.ext import commands
from gtts import gTTS
from asyncio import sleep

def setup(Bot):
    
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

    Bot.command_info.update({"text_to_speech":{
        "aliases":["text_to_speech", "tts"],
        "syntax":"<text>",
        "usage":"Converts the text given into speech, and sends it via a .mp3 file.",
        "category":"fun"
    }})
    @commands.command(name="text_to_speech", aliases=['tts'])
    async def _text_to_speech(ctx, *, text):
        async with ctx.typing():
            tts = gTTS(text = text, tld=random.choice(tld_list))
            tmp_file=tempfile.NamedTemporaryFile(delete=True, suffix=".mp3")
            tts.save(tmp_file.name)
            await ctx.send(file=discord.File(tmp_file.name))
            tmp_file.close()

    Bot.add_command(_text_to_speech)         
                
                




                
                
                