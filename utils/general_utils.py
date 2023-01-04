import random, discord, aiohttp, math
from typing import Union


def is_owner():
    async def actual_check(interaction: discord.Interaction):
        return await interaction.client.is_owner(interaction.user)
    return discord.app_commands.check(actual_check)

#invite_link = "https://discord.com/api/oauth2/authorize?client_id=849543878059098144&permissions=416578137154&scope=bot"

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
    cobalt = 0x0047ab
    indigo = 0x4B0082
    blue = 0x2298D3
    lime = 0x00FF88

#utils file for functions used repeatadly across command files.

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

item_plural = lambda value, amount: ((value['plural'][1] if amount != 1 or amount == 'all' else value['plural'][0]).replace("%", value["display_name"]))

#1st 2nd 3rd etc
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

def si_format(num): #2.412k 3.234M etc
    if num == 0:
        return "0"
    if num == 69:   # Comedy amirite
        return "nice"
    num = round(num, -math.ceil(math.log(num, 10)-4))
    magnitude = min([20, int(math.log(num, 1000))])
    return (str(num/1000**magnitude)+' ')[:-(3 if (num/1000**magnitude)%1 == 0.0 else 1)]+['', 'k', 'M', 'B', 'T', 'Qd', 'Qn', 'Sx', 'Sp', 'Oc', 'No', 'Dc', 'UDc', 'DDc', 'TDc', 'QaDc', 'QiDc', 'SxDc', 'SpDc', 'ODc', 'NDc'][magnitude]

#kryall's user id
bot_owner_id = 479963507631194133

def Embed(author:Union[discord.Member, discord.User]=None, title:str="\u200b",description:str="", colour:str="main"):

    embed = discord.Embed(title=title, description=description, colour=Colours.transparent)
    if hasattr(Colours, colour):
        embed.colour = getattr(Colours, colour)

    return embed

def error_embed(author:Union[discord.Member, discord.User]=None, message:str="Something went wrong!", apologise:bool=True):
    seed = random.randint(1, 15) == 1
    title = random.choice([["Hey!", "Hay!"][seed], ["Uhm"+"."*random.randint(1,4)]]) if apologise == False else ["Sorry!", "Sorey!"][seed]

    desc = message+(f"\n\nUse the `report_bug` command if you want to report this as an unfixed issue." if random.randint(1,7) == 3 and apologise == True else "")
    return Embed(title=title, description=desc, colour="red", author=author)

exp_to_level = lambda exp: exp*(0.6/208)#-(((exp/1.6)-exp)/130)
level_to_exp = lambda exp: exp/(0.6/208)#-(((exp/1.6)-exp)/130)

async def send_via_webhook(channel, Bot, message, username, avatar_url, files=[], embeds=[]):
    #trim message down to the first 2000 characters
    message = message[:2000] if len(message) > 2000 else message
    webhooks = await channel.webhooks()
    webhook = [webhook for webhook in webhooks if webhook.name == f"{Bot.user.name} Webhook"]
    if len(webhook) == 0: #make webhook if it doesn't exist
        avatar = await (await aiohttp.ClientSession().get(str(Bot.user.avatar.url))).read()
        webhook = [await channel.create_webhook(name=f"{Bot.user.name} Webhook", avatar=avatar)]

    webhook = webhook[0]
    await webhook.send(message, username=username, avatar_url=avatar_url, files=files, embeds=embeds)

strf_timedelta = lambda delta: ', '.join(f"{v}{k}" for k, v in ((" Minutes", delta//60), (" Seconds", delta%60)) if v != 0)

class Controller(discord.ui.View): 
    """
    controller class for a scrollable embed view thingy
    """
    def __init__(self, identifier: str, scroll_index: int, length: int):
        super().__init__()
        label_equiv = {
            "next": "⬇",
            "previous": "⬆",
            "delete": "💥"
        }
        for name in label_equiv.keys():
            self.add_item(
                discord.ui.Button(
                    label=label_equiv[name],
                    style=discord.ButtonStyle.blurple if name != "delete" else discord.ButtonStyle.red,
                    custom_id=f"{identifier}.{name}",
                    disabled=True if  #apparently parentheses remove a bunch of python's forced indents!
                    (name == "next" and scroll_index >= length-1) 
                    or 
                    (name == "previous" and scroll_index == 0)
                    else 
                    ( #mmm eye candy
                        True if
                        (name == "delete" and length == 0)
                        else
                        False
                    )
                )
            )
    
    async def on_error(self, error, item, interaction):
        await interaction.followup.send_message(embed=error_embed(message=f"The following error occurred while your interaction:\n```py\n{error}\n```"), ephemeral=True)

def make_functions_dict(identifier: str, embed_modifier: callable, delete_function: callable):
    functions_dict = {}
    async def _next(interaction: discord.Interaction):
        await interaction.response.defer() 
        embed = interaction.message.embeds[0]

        scroll_index = int(embed.footer.text.split(" ")[1])
        length = int(embed.footer.text.split(" ")[3])
        identifier = interaction.data["custom_id"].split(".")[0]

        embed = embed_modifier(embed, scroll_index, interaction)

        view = Controller(identifier, scroll_index, length)
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

    async def _previous(interaction: discord.Interaction):
        await interaction.response.defer() 
        embed = interaction.message.embeds[0]

        scroll_index = int(embed.footer.text.split(" ")[1]) - 2
        length = int(embed.footer.text.split(" ")[3])
        identifier = interaction.data["custom_id"].split(".")[0]

        embed = embed_modifier(embed, scroll_index, interaction)

        view = Controller(identifier, scroll_index, length)
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

    async def _delete(interaction: discord.Interaction):
        await interaction.response.defer() # [(id, user_id, message, timestamp, channel_id)]
        embed = interaction.message.embeds[0]

        scroll_index = int(embed.footer.text.split(" ")[1]) - 1
        scroll_index = delete_function(scroll_index)
        length = int(embed.footer.text.split(" ")[3])

        length -= 1

        embed = embed_modifier(embed, scroll_index, interaction)
        view = Controller(interaction.data["custom_id"].split(".")[0], scroll_index, length)
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

    functions_dict["next"] = _next
    functions_dict["previous"] = _previous
    functions_dict["delete"] = _delete

    return functions_dict

def interaction_listener_generator(identifier: str, functions: dict):
    async def on_interaction(interaction: discord.Interaction):
        if "custom_id" not in interaction.data:
            return
        if not interaction.data["custom_id"].startswith(f"{identifier}."):
            return
        response_author = interaction.message.interaction.user
        if interaction.user != response_author:
            return

        if interaction.data["custom_id"].split(".")[1] in functions:
            await functions[interaction.data["custom_id"].split(".")[1]](interaction)
    
    return on_interaction
