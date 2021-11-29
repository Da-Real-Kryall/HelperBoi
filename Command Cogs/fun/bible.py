import discord, requests, datetime, django.utils.timezone, string, random
from discord.ext import commands
from utils import general_utils
from lxml import html

def setup(Bot):

    Bot.command_info.update({"bible":{
        "aliases":["bible"],
        "syntax":"<Book> <Chapter>:<Verse> [translation acronym]",
        "usage":"Scrapes the specified range of verses from the bible! uses the NIV translation by default.\nYou may use a range of numbers for the chapter or the verses, but not both at the same time.",
        "category":"fun"
    }})
    @commands.command(name="bible") #sorry for bad practice, it was late when i was writing this
    async def _bible(ctx, book, chapter_verse='', translation="NIV"):

        url = f"https://www.biblegateway.com/passage/?search={book}+{chapter_verse}&version={translation}"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        cut_tree = tree.xpath("/html/body/div[2]/div/section/div[3]/div/div[2]/section/div[1]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]")
        
        return_list = []
        in_bracket = False
        for element in cut_tree:
            for item in element.itertext():
                if str(item) == '(' or str(item)  == '[':
                    in_bracket = True
                if str(item) != '\n' and in_bracket == False and general_utils.represents_int(str(item)) == False:
                    return_list += [item]
                if str(item) == ')' or str(item) == ']':
                    in_bracket = False
        #print(return_list)

        desc_text = ''.join([elm.replace("\xa0", ' ') for elm in return_list])
        if len(desc_text) > 4093:
            desc_text = desc_text[:4093]+'...'

        if desc_text == '':
            await ctx.send(embed=general_utils.error_embed(False, "It seems you entered an invalid book, verse, chapter or translation, try something different."))
            return

        bible_embed = general_utils.format_embed(ctx.author, discord.Embed(url=url, title=f"{book.lower().capitalize()} {chapter_verse} ({translation} translation)", description=desc_text))

        await ctx.send(embed=bible_embed)

    Bot.add_command(_bible)
