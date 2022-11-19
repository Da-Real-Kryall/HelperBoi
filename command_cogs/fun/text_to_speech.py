import discord, random, tempfile
from discord.ext import commands
from discord import app_commands
from gtts import gTTS
from utils import general_utils

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
class TextToSpeech(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Text to speech cog loaded.")

    @app_commands.command(name="text_to_speech", description="Converts the text given into speech, and sends it via a .mp3 file.")
    async def _text_to_speech(self, interaction: discord.Interaction, *, text: str) -> None:
        await interaction.response.defer()
        tts = gTTS(text = text, tld=random.choice(tld_list))
        tmp_file=tempfile.NamedTemporaryFile(delete=True, suffix=".mp3")
        tts.save(tmp_file.name)
        await interaction.followup.send(file=discord.File(tmp_file.name))
        tmp_file.close()

async def setup(Bot):
    await Bot.add_cog(TextToSpeech(Bot))
                




                
                
                