import discord, os, json, requests
from utils import general_utils
from discord import app_commands
from discord.ext import commands

book_conversions = {
    "Genesis": "GEN",
    "Exodus": "EXO",
    "Leviticus": "LEV",
    "Numbers": "NUM",
    "Deuteronomy": "DEU",
    "Joshua": "JOS",
    "Judges": "JDG",
    "Ruth": "RUT",
    "1 Samuel": "1SA",
    "2 Samuel": "2SA",
    "1 Kings": "1KI",
    "2 Kings": "2KI",
    "1 Chronicles": "1CH",
    "2 Chronicles": "2CH",
    "Ezra": "EZR",
    "Nehemiah": "NEH",
    "Esther": "EST",
    "Job": "JOB",
    "Psalms": "PSA",
    "Proverbs": "PRO",
    "Ecclesiastes": "ECC",
    "Song of Solomon": "SNG",
    "Isaiah": "ISA",
    "Jeremiah": "JER",
    "Lamentations": "LAM",
    "Ezekiel": "EZK",
    "Daniel": "DAN",
    "Hosea": "HOS",
    "Joel": "JOL",
    "Amos": "AMO",
    "Obadiah": "OBA",
    "Jonah": "JON",
    "Micah": "MIC",
    "Nahum": "NAM",
    "Habakkuk": "HAB",
    "Zephaniah": "ZEP",
    "Haggai": "HAG",
    "Zechariah": "ZEC",
    "Malachi": "MAL",
    "Matthew": "MAT",
    "Mark": "MRK",
    "Luke": "LUK",
    "John": "JHN",
    "Acts": "ACT",
    "Romans": "ROM",
    "1 Corinthians": "1CO",
    "2 Corinthians": "2CO",
    "Galatians": "GAL",
    "Ephesians": "EPH",
    "Philippians": "PHP",
    "Colossians": "COL",
    "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH",
    "1 Timothy": "1TI",
    "2 Timothy": "2TI",
    "Titus": "TIT",
    "Philemon": "PHM",
    "Hebrews": "HEB",
    "James": "JAS",
    "1 Peter": "1PE",
    "2 Peter": "2PE",
    "1 John": "1JN",
    "2 John": "2JN",
    "3 John": "3JN",
    "Jude": "JUD",
    "Revelation": "REV"
}

class Bible(commands.Cog):
    def get_bible(self, version: str, book: str, chapter: int, verse: int, end_verse: int = 0) -> str:
        # get json of url
        book = book_conversions[book]
        url = f"https://api.scripture.api.bible/v1/bibles/{version}/verses/{book}.{chapter}.{verse}{'-'+f'{book}.{chapter}.{end_verse}' if end_verse != 0 else ''}?content-type=text"

        data = json.loads(requests.get(url, headers={"api-key": self.nonokey}).text)
        return data["data"]["content"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bible cog loaded.")

    def __init__(self, Bot):
        self.Bot = Bot
        try:
            with open(os.getcwd()+"/tokens.txt") as nonofile:
                self.nonokey = nonofile.readlines()[1].split(" # ")[0]
        except FileNotFoundError:
            print("Bible api key missing from tokens.txt.")
            self.nonokey = None

    @app_commands.command(name="bible", description="Scrapes the specified range of verses from the bible!")
    @app_commands.choices(
        version=[
            app_commands.Choice(name="KJV", value="de4e12af7f28f599-02"),
            app_commands.Choice(name="ASV", value="685d1470fe4d5c3b-01"),
            app_commands.Choice(name="LSV", value="01b29f4b342acc35-01"),
        ],
        #{
        #book=[
        #    app_commands.Choice(name="Genesis", value="Genesis"),
        #    app_commands.Choice(name="Exodus", value="Exodus"),
        #    app_commands.Choice(name="Leviticus", value="Leviticus"),
        #    app_commands.Choice(name="Numbers", value="Numbers"),
        #    app_commands.Choice(name="Deuteronomy", value="Deuteronomy"),
        #    app_commands.Choice(name="Joshua", value="Joshua"),
        #    app_commands.Choice(name="Judges", value="Judges"),
        #    app_commands.Choice(name="Ruth", value="Ruth"),
        #    app_commands.Choice(name="1 Samuel", value="1 Samuel"),
        #    app_commands.Choice(name="2 Samuel", value="2 Samuel"),
        #    app_commands.Choice(name="1 Kings", value="1 Kings"),
        #    app_commands.Choice(name="2 Kings", value="2 Kings"),
        #    app_commands.Choice(name="1 Chronicles", value="1 Chronicles"),
        #    app_commands.Choice(name="2 Chronicles", value="2 Chronicles"),
        #    app_commands.Choice(name="Ezra", value="Ezra"),
        #    app_commands.Choice(name="Nehemiah", value="Nehemiah"),
        #    app_commands.Choice(name="Esther", value="Esther"),
        #    app_commands.Choice(name="Job", value="Job"),
        #    app_commands.Choice(name="Psalms", value="Psalms"),
        #    app_commands.Choice(name="Proverbs", value="Proverbs"),
        #    app_commands.Choice(name="Ecclesiastes", value="Ecclesiastes"),
        #    app_commands.Choice(name="Song of Solomon", value="Song of Solomon"),
        #    app_commands.Choice(name="Isaiah", value="Isaiah"),
        #    app_commands.Choice(name="Jeremiah", value="Jeremiah"),
        #    app_commands.Choice(name="Lamentations", value="Lamentations"),
        #    app_commands.Choice(name="Ezekiel", value="Ezekiel"),
        #    app_commands.Choice(name="Daniel", value="Daniel"),
        #    app_commands.Choice(name="Hosea", value="Hosea"),
        #    app_commands.Choice(name="Joel", value="Joel"),
        #    app_commands.Choice(name="Amos", value="Amos"),
        #    app_commands.Choice(name="Obadiah", value="Obadiah"),
        #    app_commands.Choice(name="Jonah", value="Jonah"),
        #    app_commands.Choice(name="Micah", value="Micah"),
        #    app_commands.Choice(name="Nahum", value="Nahum"),
        #    app_commands.Choice(name="Habakkuk", value="Habakkuk"),
        #    app_commands.Choice(name="Zephaniah", value="Zephaniah"),
        #    app_commands.Choice(name="Haggai", value="Haggai"),
        #    app_commands.Choice(name="Zechariah", value="Zechariah"),
        #    app_commands.Choice(name="Malachi", value="Malachi"),
        #    app_commands.Choice(name="Matthew", value="Matthew"),
        #    app_commands.Choice(name="Mark", value="Mark"),
        #    app_commands.Choice(name="Luke", value="Luke"),
        #    app_commands.Choice(name="John", value="John"),
        #    app_commands.Choice(name="Acts", value="Acts"),
        #    app_commands.Choice(name="Romans", value="Romans"),
        #    app_commands.Choice(name="1 Corinthians", value="1 Corinthians"),
        #    app_commands.Choice(name="2 Corinthians", value="2 Corinthians"),
        #    app_commands.Choice(name="Galatians", value="Galatians"),
        #    app_commands.Choice(name="Ephesians", value="Ephesians"),
        #    app_commands.Choice(name="Philippians", value="Philippians"),
        #    app_commands.Choice(name="Colossians", value="Colossians"),
        #    app_commands.Choice(name="1 Thessalonians", value="1 Thessalonians"),
        #    app_commands.Choice(name="2 Thessalonians", value="2 Thessalonians"),
        #    app_commands.Choice(name="1 Timothy", value="1 Timothy"),
        #    app_commands.Choice(name="2 Timothy", value="2 Timothy"),
        #    app_commands.Choice(name="Titus", value="Titus"),
        #    app_commands.Choice(name="Philemon", value="Philemon"),
        #    app_commands.Choice(name="Hebrews", value="Hebrews"),
        #    app_commands.Choice(name="James", value="James"),
        #    app_commands.Choice(name="1 Peter", value="1 Peter"),
        #    app_commands.Choice(name="2 Peter", value="2 Peter"),
        #    app_commands.Choice(name="1 John", value="1 John"),
        #    app_commands.Choice(name="2 John", value="2 John"),
        #    app_commands.Choice(name="3 John", value="3 John"),
        #    app_commands.Choice(name="Jude", value="Jude"),
        #    app_commands.Choice(name="Revelation", value="Revelation"),
        #]
    )
    async def bible(self, interaction: discord.Interaction, version: str = "de4e12af7f28f599-02", book: str = "Genesis", chapter: int = 1, verse: int = 1, end_verse: int = 0):
        if self.nonokey == None:
            await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="The Bible api key is missing from tokens.txt."), ephemeral=True)
            return
        
        data = self.get_bible(version, book, chapter, verse, end_verse)

        bible_embed = general_utils.Embed(author=interaction.user, title=f"{book} {chapter}:{verse}{'-'+str(end_verse) if end_verse != 0 else ''}", description=data, colour="blue")

        await interaction.response.send_message(embed=bible_embed)

async def setup(Bot):
    await Bot.add_cog(Bible(Bot))