import discord, random, asyncio
from utils import general_utils, database_utils
#functions that are used in the use command.

async def eat_mushroom(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a :mushroom: toadstool, you feel :nauseated_face: nauseous..."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :bread: bread loaves, you feel :nauseated_face: nauseous..."
    else:
        embed_title = "You eat a lot of :bread: bread loaves, you feel VERY :nauseated_face: nauseous..."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,3) == 1:
        embed.description = "do you have a death wish!?"
    elif random.randint(1,6) == 3:
        embed.description = 'why would you eat this?'

    embed = general_utils.format_embed(ctx.author, embed, "yellow")

    await ctx.send(embed=embed)

    await asyncio.sleep(random.randint(1,4))
    
    embed_title = f"You :face_vomiting: {random.choice(['threw up', 'vomited'])}!"
    embed_description = "That was not very cool... (lost some :sunglasses: coolness!)"

    embed = general_utils.format_embed(ctx.author, discord.Embed(title=embed_title, description=embed_description), "red")

    await ctx.send(embed=embed)

    database_utils.alter_coolness(ctx.author.id, random.randint(-10, -1)*amount)

async def eat_bread(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a :bread: bread loaf."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :bread: bread loaves."
    else:
        embed_title = "You eat a lot of :bread: bread loaves."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,8) == 1:
        embed.description = "jeez calm down"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "bread")

    await ctx.send(embed=embed)

#bind the functions to their respective names, there is very likely a better way to do this.
reference = {
    "eat_bread": eat_bread,
    "eat_mushroom": eat_mushroom
}