import discord, random, colorsys
from discord.ext import commands
from discord import app_commands

def generate_embeds(mode: str, format: str, amount: int):
    if mode == "normal":
        colours = [discord.Colour.from_rgb(int(random.random()*255), int(random.random()*255), int(random.random()*255)) for g in range(amount)]
    elif mode == "greyscale":
        colours = [discord.Colour.from_hsv(1, 0, random.random()) for g in range(amount)]
    elif mode == "vibrant":
        colours = [discord.Colour.from_hsv(random.random(), 1, 1) for g in range(amount)]

    if format == "hex":
        embeds = [discord.Embed(title=f"#{colour.value:06X}", colour=colour) for colour in colours]
    elif format == "rgb":
        embeds = [discord.Embed(title=f"RGB({colour.r}, {colour.g}, {colour.b})", colour=colour) for colour in colours]
    elif format == "hsv":
        embeds = [discord.Embed(title=f"HSV({', '.join([str(round(x, 3)) for x in colorsys.rgb_to_hsv(float(colour.r)/255, float(colour.g)/255, float(colour.b)/255)])})", colour=colour) for colour in colours]
    
    return embeds


class RandColour(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("RandColour cog loaded.")

    @app_commands.command(name="randcolour", description="Returns randomised colour(s) based on the args given.")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="Normal", value="normal"),
            app_commands.Choice(name="Greyscale", value="greyscale"),
            app_commands.Choice(name="Vibrant", value="vibrant"),
        ],
        format=[
            app_commands.Choice(name="Hexadecimal", value="hex"),
            app_commands.Choice(name="RGB", value="rgb"),
            app_commands.Choice(name="HSV", value="hsv"),
        ],
    )
    async def _randcolour(self, interaction: discord.Interaction, mode: str="normal", format: str="hex", amount: app_commands.Range[int, 1, 10]=1) -> None:
        class Controller(discord.ui.View):
            @discord.ui.button(label="Reroll", style=discord.ButtonStyle.blurple)
            async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.edit_message(embeds=generate_embeds(mode, format, amount), view=self)
        embeds = generate_embeds(mode, format, amount)
        await interaction.response.send_message(embeds=embeds, view=Controller())

        

    #Bot.command_info.update({"randcolour":{
    #    "aliases":["randcolour", "randcolor", "rcol"],
    #    "syntax":"[amount], [mode]",
    #    "usage":"Sends an amount of embeds (within 10 and 1, defaults to 1) specified by your amount given. Each embed will show a randomized colour that can be controlled with the mode if given; 'vibrant' forces a high saturation, 'greyscale' does the opposite, and 'normal'/none allows a completely random colour set. Note that only one can be sent at a time in DMs due to lack of webhooks.",
    #    "category":"fun"
    #}})
    #@commands.command(name="randcolour", aliases=['randcolor', 'rcol'])
    #async def _randcolour(ctx, amount='1', mode='normal'):
    #    if mode not in ['normal', 'greyscale', 'vibrant']:
    #        await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Mode must be either 'normal', 'greyscale', 'vibrant', or nothing to imply the former."))
    #        return
    #    if general_utils.represents_int(amount) == False:
    #        await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"{amount} is not a valid number!"))
    #        return
    #    elif int(amount) not in range(1,11):
    #        await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"{amount} must be a valid positive integer below or equal to 10."))
    #        return
    #    amount = int(amount)
    #    colour_embeds = []
    #    if ctx.guild == None:
    #        amount = 1 #if in dm i cant use webhooks
    #    for g in range(amount):
    #        colour = 0
    #        if mode == 'normal':
    #            colour = random.randint(0,16777215)
    #        elif mode == 'greyscale':
    #            #print('test')
    #            num = random.randint(0,256)
    #            colour = sum([num*16**(g*2) for g in range(3)])
    #        elif mode == 'vibrant':
    #            colour = discord.Colour.random().value
    #        colour_embeds += [discord.Embed(title=f"#{hex(colour)[2:]}", colour=colour)]
    #    if ctx.guild != None:
    #        bot_name = ctx.guild.get_member(Bot.user.id).display_name
    #    else:
    #        bot_name = Bot.user.name
    #    if ctx.guild != None:
    #        await general_utils.send_via_webhook(ctx.channel, Bot, '', bot_name, Bot.user.avatar.url, [], colour_embeds)
    #    else:
    #        await ctx.send(embed=colour_embeds[0])
    #Bot.add_command(_randcolour)

async def setup(Bot):
    await Bot.add_cog(RandColour(Bot))
