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

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "jeez calm down"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "bread")

    await ctx.send(embed=embed)

async def eat_baguette(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a :french_bread: baguette."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :french_bread: baguettes."
    else:
        embed_title = "You eat a lot of :french_bread: baguettes."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "jeez calm down"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['\*crunch\*', 'nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "bread")

    await ctx.send(embed=embed)

async def eat_flatbread(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a :flatbread: piece of flatbread."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :flatbread: pieces of flatbread."
    else:
        embed_title = "You eat a lot of :flatbread: pieces of flatbread."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "jeez calm down"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "bread")

    await ctx.send(embed=embed)

async def eat_biscuit(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a :cookie: cookie."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :cookie: cookies."
    else:
        embed_title = "You eat a lot of :cookie: cookies."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "jeez calm down"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "bread")

    await ctx.send(embed=embed)

async def eat_banana_bread(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a <:bananabread:776722921338961956> loaf of banana bread."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} <:bananabread:776722921338961956> loaves of banana bread."
    else:
        embed_title = "You eat a lot of <:bananabread:776722921338961956> loaves of banana bread."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "jeez calm down"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "yellow")

    await ctx.send(embed=embed)

async def eat_banana(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat a :banana: banana."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :banana: bananas."
    else:
        embed_title = "You eat a lot of :banana: bananas."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "thats a lot of potassium"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "yellow")

    await ctx.send(embed=embed)

async def eat_apple(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You eat an :apple: apple."
    elif amount > 1 and amount < 1000000000:
        embed_title = f"You eat {general_utils.num_to_words(amount)} :apple: apples."
    else:
        embed_title = "You eat a lot of :apple: apples."

    embed = discord.Embed(title=embed_title)

    if amount > 150 and random.randint(1,4) == 1:
        embed.description = "this many apples a day will keep you away!"
    elif random.randint(1,6) == 3:
        embed.description = random.choice(['nom nom', 'yum!', 'om nom nom', '\*burp\*'])

    embed = general_utils.format_embed(ctx.author, embed, "yellow")

async def sample_func(ctx, Bot, amount): 
    embed = discord.Embed(title="<sample use response>", description="+1000 <:Simolean:769845739043684353> Simoleons")
    embed = general_utils.format_embed(ctx.author, embed, "yellow")
    await ctx.send(embed=embed)
    database_utils.alter_balance(ctx.author.id, 1000)

async def poke_other(ctx, Bot, amount):
    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title="Who do you want to poke with the stick?"), "wood", False))
    check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content != None and m.content != ''
    try:
        msg = await Bot.wait_for('message', timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("nevermind...")
        raise RuntimeError #error to call when function didnt do anything, so the item isnt consumed 
    user_id = await general_utils.get_user_id(Bot, ctx, msg.content, False)
    if user_id == None:
        #await ctx.send(embed=general_utils.error_embed(False, "That doesnt seem to be a valid user."))
        raise RuntimeError

    user = ctx.guild.get_member(user_id)
    poke_title = f"You poke {user.display_name if ctx.author != user else 'yourself'} with the stick!"
    poke_desc = f"That wasnt very cool, you and {user.display_name if ctx.author != user else 'yourself'} lost some :sunglasses: coolness!"

    poke_embed = discord.Embed(title=poke_title, description=poke_desc)
    poke_embed = general_utils.format_embed(ctx.author, poke_embed, "wood")
    await ctx.send(embed=poke_embed)

    database_utils.alter_coolness(user_id, -random.randint(3,10))
    database_utils.alter_coolness(ctx.author.id, -random.randint(3,10))

async def throw_at_other(ctx, Bot, amount):
    item_name = random.choice(['small rock', 'pebble'])
    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Who do you want to throw the {item_name} at?"), "silver", False))
    check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content != None and m.content != ''
    try:
        msg = await Bot.wait_for('message', timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("nevermind...")
        raise RuntimeError #error to call when function didnt do anything, so the item isnt consumed 
    user_id = await general_utils.get_user_id(Bot, ctx, msg.content, False)
    if user_id == None:
        #await ctx.send(embed=general_utils.error_embed(False, "That doesnt seem to be a valid user."))
        raise RuntimeError

    user = ctx.guild.get_member(user_id)
    throw_title = f"You throw the {item_name} at {user.display_name if ctx.author != user else 'yourself'}!"
    throw_desc = f"That wasnt very cool, you "
    if random.randint(1,2) == 1:
        throw_desc += f"and {user.display_name if ctx.author != user else 'yourself'} lost some :sunglasses: coolness!"
        database_utils.alter_coolness(user_id, -random.randint(3,10))
    else:
        throw_title += " Thankfully, it misses..."
        throw_desc += "lost some :sunglasses: coolness!"

    throw_embed = discord.Embed(title=throw_title, description=throw_desc)
    throw_embed = general_utils.format_embed(ctx.author, throw_embed, "silver")
    await ctx.send(embed=throw_embed)

    database_utils.alter_coolness(ctx.author.id, -random.randint(3,20))


#bind the functions to their respective names, there is very likely a better way to do this.
reference = {
    "eat_mushroom": eat_mushroom,
    "eat_bread": eat_bread,
    "eat_baguette": eat_baguette,
    "eat_flatbread": eat_flatbread,
    "eat_biscuit": eat_biscuit,
    "eat_banana_bread": eat_banana_bread,
    "eat_banana": eat_banana,
    "eat_apple": eat_apple,
    "sample_func": sample_func,
    "poke_other": poke_other,
    "throw_at_other": throw_at_other,
}