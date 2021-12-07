import random, discord, datetime, django.utils.timezone, asyncio
from utils import database_utils



#colours to be used in most embeds
class Colours:
    main = 0xBAFDFC
    yellow = 0xFACE0A   #0xF4D640
    green = 0x09DF17
    red = 0xEA1510
    charcoal = 0x2E2D2B
    transparent = 0x2F3136
    bread = 0xF0BF6A
    wood = 0x663300
    silver = 0xE2E2E2

#utils file for functions used repeatadly across command files.
def error_embed(apologise:bool, message:str):
    return discord.Embed(timestamp=datetime.datetime.now(django.utils.timezone.utc), colour=Colours.main, title=("Sorry!" if apologise else "Hey!") if random.randint(1, 15) != 1 else ("Sorey!" if apologise else "Hay!"), description=message+(f"\n\nUse the `report_bug` command if you want to report this as an unfixed issue." if random.randint(1,10) == 3 else ""))

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#1st 2nd 3rd etc
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

#kryall's user id
bot_owner_id = 479963507631194133

#by default, add timestamp, colour and footer to embed.
def format_embed(author:discord.Message.author, embed:discord.Embed, colour:str="main", footer:bool=True,timestamp:bool=True):
    if embed.colour == discord.Embed.Empty:
        if hasattr(Colours, colour):
            embed.colour = getattr(Colours, colour)
    if footer == True and embed.footer != discord.Embed.Empty:
        embed.set_footer(text=f'Requested by {author.display_name}', icon_url=author.avatar_url)
    if embed.timestamp == discord.Embed.Empty and timestamp == True:
        embed.timestamp = datetime.datetime.now(django.utils.timezone.utc)
    return embed

async def get_user_id(Bot, ctx, text, check_all_users=False, lenient=False): #lenient means error messages will be avoided, further prompts will be minimal, and plaintext that doesnt specify a single person is also accepted.
    if ctx.guild == None and check_all_users == False:
        raise TypeError("you must be checking all users if in a dm, there isnt a guild to check names from!")
    else:
        if text == None or text == '':
            return ctx.author.id
        #check if input is a ping
        if text[:3] == "<@!" and text[-1:] == ">" and represents_int(text[3:-1]):
            text = text[3:-1]
        elif text[:2] == "<@" and text[-1:] == ">" and represents_int(text[2:-1]):
            text = text[2:-1]

        user_ids = {}
        if ctx.guild != None:
            for member in ctx.guild.members:
                if text.casefold() == member.display_name.casefold():
                    user_ids.update(
                        {member.id: member.display_name}
                    ) 
            _user_ids = dict(user_ids)
            if text in user_ids.values():
                for key, value in user_ids.items():
                    if value != text:
                        _user_ids.pop(key)
            user_ids = dict(_user_ids)
            if len(user_ids) == 0:
                for member in ctx.guild.members:
                    if member.display_name.casefold().startswith(text.casefold()):
                        user_ids.update( 
                        {member.id: member.display_name}
                    )
        if len(user_ids) == 0 and represents_int(text) == True:
            user = Bot.get_user(int(text))
            if user != None:
                user_ids.update({user.id: user.name})
                
        if check_all_users == True:
            #require it to be an id
            #if represents_int(text) == False and len(user_ids) == 0:
            #    if ctx.guild != None:
            #        await ctx.send("This command checks almost ALL discord users and thus integer ids are required for checking users not in the current server.")
            #    else:
            #        await ctx.send("This command checks almost ALL discord users and thus integer ids are required for specifying people.")
            #    return
            if represents_int(text) == True:
                user = await Bot.fetch_user(int(text))
                if user != None:
                    user_ids.update({user.id: user.name})
    if len(user_ids) == 0:
        if lenient==False:
            await ctx.send(embed=error_embed(True, "No users were found."))
            return None
        else:
            return text
    elif len(user_ids) > 1 and lenient == False:
        await ctx.send("Please say the number corresponding to whichever of the possible users you meant:\n"+'\n'.join([f"[{index}] \"{str(ctx.guild.get_member(value))}\"" for index, value in enumerate(list(user_ids.keys()))]))
        
        check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author
        try:
            msg = await Bot.wait_for('message', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("nevermind...")
            return None
        
        id_list = [value for value in list(user_ids.keys())]
        if represents_int(msg.content):
            if int(msg.content) < len(id_list):
                user_id = [value for value in list(user_ids.keys())][int(msg.content)]
            else:
                await ctx.send(embed=error_embed(False, "Please pick a number that was listed."))
                return None
        else:
            await ctx.send(embed=error_embed(False, "Please pick a number that was listed."))
            return None
    else:
        user_id = int(list(user_ids.keys())[0])
    return user_id

def num_to_words(num): #this code is not mine, it was taken from "https://www.quora.com/How-do-I-convert-numbers-to-words-in-Python" as i could not be bothered to write my own function for this lol
    if num == 69:
        return "nice" #dont judge me
    else:
        under_20 = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'] 
        tens = ['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'] 
        above_100 = {100: 'hundred and',1000:'thousand,', 1000000:'million', 1000000000:'billion'} 
    
        if num < 20: 
             return under_20[num] 

        if num < 100: 
            return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10]) 
    
        # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550 
        pivot = max([key for key in above_100.keys() if key <= num]) 
    
        return num_to_words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num_to_words(num%pivot))