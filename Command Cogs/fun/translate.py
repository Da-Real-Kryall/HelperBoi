import discord, json, string
from discord.ext import commands
from utils import general_utils


def setup(Bot):

    with open("Recources/json/translations.json") as file:
        charset_json = json.load(file)

    Bot.command_info.update({"translate":{
        "aliases":["translate", "tl"],
        "syntax":"<from> <to>\"<text>\"",
        "usage":"A simple translator between different representations of **ENGLISH** text.\nTranslates the given text from the first type specified in '<from>' to the type specified in '<to>'.\nThe choices for translation are \"wingdings\", \"plaintext\", and \"morse\"",
        "category":"fun"
    }})

    @commands.command(name="translate", aliases=["tl"])
    async def _translate(ctx, type_from,  type_to, *, text="Give me text to translate you smoothbrain"):
        
        charset_from = charset_json[type_from]
        charset_to = charset_json[type_to]

        flipped_charset_to = {}
        for item in charset_to["charlist"].items():
            flipped_charset_to.update({str(item[1]): item[0]})

        return_text = []

        if charset_to["case_sensitive"] == False or charset_from["case_sensitive"] == False:
            text = text.lower()

        text = text.split(charset_from["separator"]) if charset_from["separator"] != "" else list(text)
 
        for char in text:
            if char not in list(charset_from["charlist"].keys()):
                return_text += [flipped_charset_to["76"]]
            else:
                return_text += [flipped_charset_to[str(charset_from["charlist"][char])]]
                
        return_text = charset_to["separator"].join(return_text)

        translate_embed = discord.Embed(title='Translation Result:', description="```"+return_text+"```")
        translate_embed = general_utils.format_embed(ctx.author, translate_embed)
        await ctx.send(embed=translate_embed)

    Bot.add_command(_translate)
