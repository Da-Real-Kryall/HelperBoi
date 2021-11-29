
import discord, string, requests
from lxml import html
from discord.ext import commands 
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"wiki":{
        "aliases":["wikipedia", "wiki"],
        "syntax":"<thing>",
        "usage":"Scrapes data from either en.wikipedia.org or simple.wikipedia.org and returns a summary of the thing given!",
        "category":"utility"
    }})
    @commands.command(name="wiki", aliases=["wikipedia"])
    async def _wiki(ctx, *, thing):
        thing = '_'.join(thing.capitalize().split())
        with ctx.typing():
            page = requests.get(f"https://simple.wikipedia.org/wiki/{thing}")
            tree = html.fromstring(page.content)
            if ''.join(tree.xpath('//*[@id="mw-content-text"]/div[1]/p[1]//text()')) == '':
                page = requests.get(f"https://en.wikipedia.org/wiki/{thing}")
                tree = html.fromstring(page.content)

                if ''.join(tree.xpath('//*[@id="mw-content-text"]/div[1]/p[1]//text()')) == '':
                    await ctx.send(embed=discord.Embed(title='Failed! :(', description='No pages were found with the query', colour=0xea1510))
                    return
                else:
                    desc = ''.join(tree.xpath('//*[@id="mw-content-text"]/div[1]/p[1]//text()'))
                    if len(desc) >= 2048:
                        desc = desc[:2045]+'...'
                    wiki_embed = discord.Embed(url=f"https://en.wikipedia.org/wiki/{thing}", title=f"Summary about {thing}", description=desc)
                    wiki_embed = general_utils.format_embed(ctx.author, wiki_embed)
                    await ctx.send(embed=wiki_embed)
                    return
            else:
                desc = ''.join(tree.xpath('//*[@id="mw-content-text"]/div[1]/p[1]//text()'))
                if len(desc) >= 2048:
                    desc = desc[:2045]+'...'
                wiki_embed = discord.Embed(url=f"https://simple.wikipedia.org/wiki/{thing}", title=f"Summary about {thing}", description=desc)
                wiki_embed = general_utils.format_embed(ctx.author, wiki_embed)
                await ctx.send(embed=wiki_embed)

    Bot.add_command(_wiki)
