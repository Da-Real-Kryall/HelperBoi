import discord, random
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"randcolour":{
        "aliases":["randcolour", "randcolor", "rcol"],
        "syntax":"[amount], [mode]",
        "usage":"Sends an amount of embeds (within 10 and 1, defaults to 1) specified by your amount given. Each embed will show a randomized colour that can be controlled with the mode if given; 'vibrant' forces a high saturation, 'greyscale' does the opposite, and 'normal'/none allows a completely random colour set. Note that only one can be sent at a time in DMs due to lack of webhooks.",
        "category":"fun"
    }})
    @commands.command(name="randcolour", aliases=['randcolor', 'rcol'])
    async def _randcolour(ctx, amount='1', mode='normal'):
        if mode not in ['normal', 'greyscale', 'vibrant']:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Mode must be either 'normal', 'greyscale', 'vibrant', or nothing to imply the former."))
            return
        if general_utils.represents_int(amount) == False:
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"{amount} is not a valid number!"))
            return
        elif int(amount) not in range(1,11):
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, f"{amount} must be a valid positive integer below or equal to 10."))
            return
        amount = int(amount)
        colour_embeds = []
        if ctx.guild == None:
            amount = 1 #if in dm i cant use webhooks
        for g in range(amount):
            colour = 0
            if mode == 'normal':
                colour = random.randint(0,16777215)
            elif mode == 'greyscale':
                #print('test')
                num = random.randint(0,256)
                colour = sum([num*16**(g*2) for g in range(3)])
            elif mode == 'vibrant':
                colour = discord.Colour.random().value
            colour_embeds += [discord.Embed(title=f"#{hex(colour)[2:]}", colour=colour)]
        if ctx.guild != None:
            bot_name = ctx.guild.get_member(Bot.user.id).display_name
        else:
            bot_name = Bot.user.name
        if ctx.guild != None:
            await general_utils.send_via_webhook(ctx.channel, Bot, '', bot_name, Bot.user.avatar.url, [], colour_embeds)
        else:
            await ctx.send(embed=colour_embeds[0])
    Bot.add_command(_randcolour)