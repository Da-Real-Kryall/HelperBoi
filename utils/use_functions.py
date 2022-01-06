import discord, random, asyncio, os, json
from utils import general_utils, database_utils
#functions that are used in the use and eat commands.

reference = {
    "food": {},
    "other": {}
}

def create_eat_function(upper_bound:int=1000000000, colour:str="main", chance_event:list=[0.0, lambda: None], excess:list=[0.0, float("inf"), []], item_name:str="item_name"):
    with open(os.getcwd()+"/Recources/json/items.json") as file:
        item_json = json.loads(file.read())
    item = item_json[item_name]
    async def use_function(message, amount): #excess is [chance, upper_bound, [possible messages]]
        embed_description = None
        if amount == 1:
            embed_title = f"You eat a{'n' if item['display_name'][0].lower() in ['a', 'e', 'i', 'o', 'u'] else ''} {item['emoji']} {general_utils.item_plural(item, 1)}."
        elif amount > 1 and amount < upper_bound:
            embed_title = f"You eat {amount} {item['emoji']} {general_utils.item_plural(item, amount)}"
        else:
            embed_title = f"You eat a lot of {item['emoji']} {general_utils.item_plural(item, amount)}"
            if random.random() < excess[0]:
                embed_description = random.choice(excess[2])
        if amount > excess[1]:
            embed_description = random.choice(excess[2])
        embed = discord.Embed(title=embed_title)
        if embed_description != None:
            embed.description=embed_description
        elif random.random() < 0.5:
            embed.description = random.choice(['\*crunch\*', 'yum!', 'om nom nom', '\*burp\*']) #default messages
        embed = general_utils.format_embed(message.author, embed, colour)
        if random.random() < chance_event[0]:
            await chance_event[1](message, amount)
        await message.channel.send(embed=embed)
    reference["food"].update({f"eat_{item_name}": use_function})

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
    if user.bot:
        await ctx.send(embed=general_utils.error_embed(True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
        return
    poke_title = f"You poke {user.display_name if ctx.author != user else 'yourself'} with the stick!"
    poke_desc = f"That wasnt very cool, you and {user.display_name if ctx.author != user else 'yourself'} lost some :sunglasses: coolness!"

    poke_embed = discord.Embed(title=poke_title, description=poke_desc)
    poke_embed = general_utils.format_embed(ctx.author, poke_embed, "wood")
    await ctx.send(embed=poke_embed)
    giveamount = -random.randint(3,50)
    cur_amount = database_utils.alter_coolness(ctx.author.id, giveamount)[0]
    await general_utils.level_check(giveamount, cur_amount, ctx.channel, ctx.author)
    giveamount = -random.randint(3,50)
    cur_amount = database_utils.alter_coolness(user_id, giveamount)[0]
    await general_utils.level_check(giveamount, cur_amount, ctx.channel, user)

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
    if user.bot:
        await ctx.send(embed=general_utils.error_embed(True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
        return
    throw_title = f"You throw the {item_name} at {user.display_name if ctx.author != user else 'yourself'}!"
    throw_desc = f"That wasnt very cool, you "
    if random.randint(1,2) == 1:
        throw_desc += f"and {user.display_name if ctx.author != user else 'yourself'} lost some :sunglasses: coolness!"
        giveamount = -random.randint(80, 140)
        cur_amount = database_utils.alter_coolness(user_id, giveamount)[0]
        await general_utils.level_check(giveamount, cur_amount, ctx.channel, user)
    else:
        throw_title += " Thankfully, it misses..."
        throw_desc += "lost some :sunglasses: coolness!"

    throw_embed = discord.Embed(title=throw_title, description=throw_desc)
    throw_embed = general_utils.format_embed(ctx.author, throw_embed, "silver")
    await ctx.send(embed=throw_embed)

    giveamount = -random.randint(80, 140)
    cur_amount = database_utils.alter_coolness(ctx.author.id, giveamount)[0]
    await general_utils.level_check(giveamount, cur_amount, ctx.channel, ctx.author)

async def equip_starsticker(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You put on a golden :star: starsticker."
    else:
        embed_title = f"You put on {amount} golden :star: starstickers."
    embed_description = f"You feel quite {random.choice(['dapper', 'cool', 'good about yourself'])}, your coolness has increased a little!"
    give_amount = sum([random.randint(1, 25)]*amount)
    cur_amount, delta = database_utils.alter_coolness(ctx.author.id, give_amount)
    await general_utils.level_check(give_amount, cur_amount, ctx.channel, ctx.author)
    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=embed_title, description=embed_description), "yellow"))
    
async def equip_sunglasses(ctx, Bot, amount):
    if amount == 1:
        embed_title = "You put on a pair of :dark_sunglasses: sunglasses."
    else:
        embed_title = f"You put on {amount} pairs of :dark_sunglasses: sunglasses."
    embed_description = f"You feel quite {random.choice(['dapper', 'cool', 'good about yourself'])}, your coolness has increased!"
    give_amount = sum([random.randint(1, 60)]*amount)
    cur_amount, delta = database_utils.alter_coolness(ctx.author.id, give_amount)
    await general_utils.level_check(give_amount, cur_amount, ctx.channel, ctx.author)
    await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=embed_title, description=embed_description), "charcoal"))

async def shake_eightball(ctx, Bot, amount):
    message = await ctx.send(embed=discord.Embed(title="You shake the magic 8-ball vigorously...", description="A message is appearing in the window...", colour=general_utils.Colours.indigo))
    await asyncio.sleep(random.randint(2, 7))
    responses = [
        "Yes.",
        "No.",
        "bruh no",
        "obviously yes",
        "i'd say 1.5",
        "i cannot be certain",
        "reception bad try again later",
        "yes'nt",
        "certainly",
        "(the little internal die with the answers landed on an edge)",
        "yes, of course",
        "my sources say no."
    ]
    await message.edit(embed=general_utils.format_embed(ctx.author, discord.Embed(title="The 8-ball has given its response:", description=f"\"{random.choice(responses)}\""), "cobalt"))
    #await ctx.send(embed=embed)

async def lsd_effect(message):
    if random.random() < 0.5:
        pass#do lsd effect
    else: #you throw up the mushroom
        await asyncio.sleep(random.randint(1,4))

        embed_title = f"You :face_vomiting: {random.choice(['threw up', 'vomited'])}{random.choice(['!', '...'])}"
        embed_description = "That was not very cool..."

        embed = general_utils.format_embed(message.channel.author, discord.Embed(title=embed_title, description=embed_description), "red")

        await message.channel.send(embed=embed)
        giveamount = random.randint(-120, -1)
        cur_amount = database_utils.alter_coolness(message.author.id, giveamount)[0]
        await general_utils.level_check(giveamount, cur_amount, message.channel, message.author)

eat_functions_data = [
    {"colour":"yellow", "excess":[0.8, 50, ["Thats a lotta potassium..."]], "item_name":"banana"},
    {"colour":"red", "excess":[0.9, 100, ["This many apples a day will keep you away!"]], "item_name":"apple"},
    {"colour": "bread", "excess": [0.5, 175, ["jeez calm down"]], "item_name":"bread"},
    {"colour": "bread", "excess": [0.5, 175, ["jeez calm down"]], "item_name":"baguette"},
    {"colour": "bread", "excess": [0.5, 175, ["jeez calm down"]], "item_name":"flatbread"},
    {"colour": "yellow", "excess": [0.8, 50, ["jeez calm down"]], "item_name":"bananabread"},
    {"colour": "bread", "excess": [0.9, 50, ["thats a lotta calories"]], "item_name":"biscuit"},
    {"colour": "yellow", "excess": [0.9, 50, ["hope you arent lactose intolerant"]], "item_name":"cheese"},
    {"colour": "red", "excess": [0.9, 100, ["\*munchy munch\*"]], "item_name":"tomato"},
    {"colour": "red", "excess": [0.9, 50, ["thats a lotta calories"]], "item_name":"pizza"},
    {"colour": "bread", "excess": [1, 10, ["how many individual pizza slices was that?", "expensive meal..."]], "item_name":"pizzacake"},
    {"colour": "red", "excess": [0.6, 1, ["why would you eat this?"]], "chance_event": [1.1, lsd_effect], "item_name":"mushroom"}
]

for func_data in eat_functions_data:
    create_eat_function(**func_data)

reference["other"].update({
    "sample_func": sample_func,
    "poke_other": poke_other,
    "throw_at_other": throw_at_other,
    "equip_starsticker": equip_starsticker,
    "equip_sunglasses": equip_sunglasses,
    "shake_eightball": shake_eightball
})