import discord, os, json, random
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    with open(os.getcwd()+"/Recources/json/weeb_gif_ids.json") as file:
        gif_json = json.loads(file.read())

    Bot.command_info.update({"cuddle":{
        "aliases":["cuddle"],
        "syntax":"<user>",
        "usage":"Lets you cuddle the given person, accepts ideally mentions, though ids and plaintext are also supported.",
        "category":"fun"
    }})
    @commands.guild_only()
    @commands.command(name="cuddle")
    async def _cuddle(ctx, *, user=''):
        user_id = await general_utils.get_user_id(Bot, ctx, user, False, True)
        if type(user_id) == str:
            user = user_id
        else: #id must be int
            user = ctx.guild.get_member(user_id)
            user = user.display_name
        if user == ctx.author.display_name:
            user = "yourself"
        

        embed_title = random.choice(["cuddled %s", "you cuddle %s", "you give %s a cuddle"]) % user
        if random.randint(1,3) != 1:
            embed_title = embed_title.capitalize()
            
        embed_title += random.choice(['.', '!', '...', ''])

        cuddle_embed = discord.Embed(title=embed_title, colour=discord.Colour.random())
        cuddle_embed.set_image(url=f"https://cdn.weeb.sh/images/{random.choice(gif_json['cuddle'])}")

        cuddle_embed = general_utils.format_embed(ctx.author, cuddle_embed, footer=False)
        cuddle_embed.set_footer(text="Powered by weeb.sh")

        await ctx.send(embed=cuddle_embed)

    Bot.add_command(_cuddle)