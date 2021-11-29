import random, discord, datetime, django.utils.timezone

#colours to be used in most embeds
class Colours:
    main = 0xBAFDFC
    yellow = 0xFACE0A   #0xF4D640
    green = 0x09DF17
    red = 0xEA1510

#utils file for functions used repeatadly across command files.
def error_embed(apologise:bool, message:str):
    return discord.Embed(timestamp=datetime.datetime.now(django.utils.timezone.utc), colour=Colours.main, title=("Sorry!" if apologise else "Hey!") if random.randint(1, 15) != 1 else ("Sorey!" if apologise else "Hay!"), description=message)

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#1st 2nd 3rd etc
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])


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

def get_player_id(get_user, ctx, text: str, check_all_users=False):
    if check_all_users==False:
        if ctx.guild == None:
            raise TypeError
        else:
            returnlist = {}
            for member in ctx.guild.members:
                if text.casefold() == member.display_name.casefold():
                    returnlist.update(
                        {member.id: member.display_name}
                    ) 
            _returnlist = dict(returnlist)
            if text in returnlist.values():
                for key, value in returnlist.items():
                    if value != text:
                        _returnlist.pop(key)
            returnlist = dict(_returnlist)
        if len(returnlist) == 0:
            for member in ctx.guild.members:
                if member.display_name.casefold().startswith(text.casefold()):
                    returnlist.update( 
                    {member.id: member.display_name}
                )
        if len(returnlist) == 0 and represents_int(text) == True:
            user = get_user(int(text))
            if user != None:
                returnlist.update({user.id: user.name})

    return returnlist