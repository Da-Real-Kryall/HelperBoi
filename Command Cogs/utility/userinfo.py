import discord, os, json
from discord.ext import commands
from utils import general_utils, database_utils

def setup(Bot):

    badge_dict = {
        "hypesquad_bravery": "<:Bravery:767970207942574080>",
        "hypesquad_brilliance": "<:Brilliance:767970221801472020>",
        "hypesquad_balance":"<:Balance:767970262825435146>",
        "early_verified_bot_developer":"<:Early_Verified_Bot_Developer:767970253288112148>",
        "verified_bot_developer": "<:Early_Verified_Bot_Developer:767970253288112148>",
        "bug_hunter": "<:Bughunter_Level1:767970274095136818>",
        "bug_hunter_level_2": "<:Bughunter_Level2:767970285755957259>",
        "staff": "<:Employee:767970387706773504>",
        "early_supporter": "<:Early_Supporter:767970488851890200>"
    }
    statuses_dict = {
        "dnd":':red_circle:',
        'online':':green_circle:',
        'offline':':new_moon:',
        'idle':':yellow_circle:',
        'streaming':'<:streaming:916986928220475393>'
    }

    Bot.command_info.update({"userinfo":{
        "aliases":["userinfo", "uinfo", "whois"],
        "syntax":"[user]",
        "usage":"Will return a bunch of info about the given user or the author if no user is given.",
        "category":"utility"
    }})
    #@commands.guild_only()
    @commands.command(name="userinfo", aliases=["uinfo", "whois"])
    async def _userinfo(ctx, *, user=None):
        user_id = await general_utils.get_user_id(Bot, ctx, user, True)
        if user_id == None:
            return
        if ctx.guild != None:
            user = ctx.guild.get_member(user_id)
        else:
            user = None
        if user == None:
            user = await Bot.fetch_user(user_id)
        
        #base embed
        user_info_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Info about {f'{statuses_dict[user.status[0]]} ' if type(user) == discord.Member else ''}{user.name}#{user.discriminator}:"))
        if user.bot:
            user_info_embed.title += f"{'<:CHECK:768779393509097484>' if user.public_flags.verified_bot else ''}<:B_:768779404888899605><:O_:768779415852417034><:T_:768779427487416341>"
        if type(user) == discord.Member:
            if user.colour.value != 0:
                user_info_embed.colour = user.colour.value
            #user_info_embed.title += f" {statuses_dict[user.status[0]]}"

        #embed icon
        user_info_embed.set_thumbnail(url=user.avatar_url)

        user_info = {}
        
        #member only info (only works for users in the guild the message was sent in)
        if type(user) == discord.Member:
            #status
            status = ""
            #print([user.status[0]])
            if user.status[0] != 'offline' and user.activity != None:
                #print("test2")
                if user.activity.type == discord.ActivityType.custom:
                    user_info.update({"Activity:": f"\"{user.activity.emoji+' ' if user.activity.emoji != None else ''}{user.activity.name if user.activity.name != None else ''}\""})
                
                elif user.activity.type == discord.ActivityType.listening:   
                    #excuse the switch-like hardcoding, its the least messy way i can think of.
        
                    if hasattr(user.activity, 'title') and hasattr(user.activity, 'artist') and hasattr(user.activity, 'name'):
                        user_info.update({"Activity:": f"Listening to {user.activity.title} By {user.activity.artist} on {user.activity.name}."})
                    
                    elif hasattr(user.activity, 'title') and hasattr(user.activity, 'name'):
                        user_info.update({"Activity:": f"Listening to {user.activity.title} on {user.activity.name}."})

                    elif hasattr(user.activity, 'title') and hasattr(user.activity, 'artist'):
                        user_info.update({"Activity:": f"Listening to {user.activity.title} By {user.activity.artist}."})

                    elif hasattr(user.activity, 'name') and hasattr(user.activity, 'artist'):
                        user_info.update({"Activity:": f"Listening to a song by {user.activity.artist} on {user.activity.name}."})

                    elif hasattr(user.activity, 'name'):
                        user_info.update({"Activity:": f"Listening to {user.activity.name}."})

                    elif hasattr(user.activity, 'title'):
                        user_info.update({"Activity:": f"Listening to {user.activity.title}."})

                    elif hasattr(user.activity, 'artist'):
                        user_info.update({"Activity:": f"Listening to a song by {user.activity.artist}."})
                
                elif user.activity.type == discord.ActivityType.playing:
                    user_info.update({"Activity:": f"Playing {user.activity.name}."})
                
                elif user.activity.type == discord.ActivityType.watching:
                    user_info.update({"Activity:": f"Watching {user.activity.name}."})
                    
            #time joined the server  
            user_info.update({"Server join date:": f"<t:{int(user.joined_at.timestamp())}:f> (<t:{int(user.joined_at.timestamp())}:R>)"})

            #roles
            roles = []
            for role in user.roles:
                roles += [f"<@&{role.id}>"]
            roles = ', '.join(roles[1:])
            if len(roles) == 0:
                roles = "None :("
            user_info.update({"Roles:": roles})
            

        #user info (works in dms etc):

        #awards
        awards = "".join([badge_dict[badge[0]] for badge in user.public_flags.all() if badge[0] in list(badge_dict.keys())])
        user_info.update({"Badges:": awards if awards != "" else "None :("})

        #mention
        user_info.update({"Mention:": str(user.mention)})

        #id
        user_info.update({"Id:": str(user.id)})

        #account creation date
        user_info.update({"Account created at:": f"<t:{int(user.created_at.timestamp())}:f> (<t:{int(user.created_at.timestamp())}:R>)"})
        
        #economy stuff

        #boops
        user_info.update({"Boops:": f"{general_utils.num_to_words(database_utils.fetch_boops(user_id))} boop{'s' if database_utils.fetch_boops(user_id) != 1 else ''}"})
        if database_utils.fetch_setting("users", user_id, "economy_invisibility") == False or ctx.author.id == user_id:
            with open(os.getcwd()+"/Recources/json/items.json") as file:
                item_json = json.loads(file.read())

            #coolness
            level = database_utils.fetch_coolness(user_id)[1]
            user_info.update({"Level:": f"Coolness level {level} :{'sunglasses' if level >= 0 else 'confused'}:"})
        
            #balance
            user_info.update({"Balance:": f"§{database_utils.fetch_balance(user_id)}"})

            #inventory
            inv_data = database_utils.fetch_inventory(user_id, True)
            inventory_string = []
            for item, quantity in inv_data.items():
                if quantity != 0:
                    inventory_string += [f"{item_json[item]['emoji']} {item_json[item]['display_name']} x{quantity}"]
            if len(inventory_string) == 0:
                user_info.update({"Inventory:": "Nothing :("})
            else:
                user_info.update({"Inventory:": "\n".join(inventory_string)})
        else: #add fields except <hidden> is their value
            user_info.update({"Level:": "<hidden>"})
            user_info.update({"Balance:": f"<hidden>"})
            user_info.update({"Inventory:": "<hidden>"})
        

        for key, value in user_info.items():
            user_info_embed.add_field(name=key, value=value)

        await ctx.send(embed=user_info_embed)

    Bot.add_command(_userinfo)
