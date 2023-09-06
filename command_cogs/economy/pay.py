import discord
from discord.ext import commands
from discord import app_commands
from utils import general_utils, database_utils

class Pay(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pay Cog Loaded")

    @app_commands.command(name="pay", description="Pays some amount of money to a given user. Amount defaults to all of your money.")
    async def _pay(self, interaction: discord.Interaction, user: discord.User, amount: app_commands.Range[int, 1]):
        """
        
        """
        payer_balance = database_utils.fetch_user_data(interaction.user.id, "balance")
        if amount == None:
            amount = payer_balance
        elif amount > payer_balance:
            await interaction.response.send_message(embed=general_utils.error_embed(interaction.user, message="You don't have enough money to do that!", apologise=False), ephemeral=True)
            return
        
        recipient_balance = database_utils.fetch_user_data(user.id, "balance")
        
        database_utils.set_user_data(interaction.user.id, "balance", payer_balance - amount)
        database_utils.set_user_data(user.id, "balance", recipient_balance + amount)
        
        response_embed = general_utils.Embed(author=interaction.user, title=f"Transaction Successful.", colour="yellow")
        
        response_embed.add_field(name=f"{interaction.user.name}:", value=f"-{general_utils.si_format(amount)} <:Simolean:769845739043684353> Simolean{'s' if abs(amount) != 1 else ''}", inline=True)
        response_embed.add_field(name=f"{user.name}:", value=f"+{general_utils.si_format(amount)} <:Simolean:769845739043684353> Simolean{'s' if abs(amount) != 1 else ''}", inline=True)
        
        await interaction.response.send_message(embed=response_embed, ephemeral=False)

async def setup(Bot):
    await Bot.add_cog(Pay(Bot))






#import discord, json, os, asyncio, random
#from discord.ext import commands
#from utils import general_utils, database_utils
#
#def setup(Bot):
#
#    Bot.command_info.update({"pay":{
#        "aliases":["pay"],
#        "syntax":"<user> <amount>",
#        "usage":"Will send your specified amount of simoleons to the given user, with confirmation. The amount must be a valid positive integer equal to or lower than your current balance, or 'all' if you, for some reason, want to give all of your money to the given user.",
#        "category":"economy"
#    }})
#    @commands.command(name="pay")
#    async def _pay(ctx, user, amount):
#        error_embed = general_utils.error_embed(Bot, ctx, ctx.author, "Please give a valid positive integer or 'all' as the amount of simoleons to give.")
#        if general_utils.represents_int(amount):
#            if int(amount) < 1 and ctx.author.id != general_utils.bot_owner_id:
#                await ctx.send(embed=error_embed)
#                return
#        elif amount != "all":
#            await ctx.send(embed=error_embed)
#            return
#
#        user_id = await general_utils.get_user_id(Bot, ctx, user, False)
#        if user_id == None:
#            return
#        user = await Bot.fetch_user(user_id)
#        if user.bot:
#            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "The user specified is a bot, and thus doesn't and won't have any economy data."))
#            return
#
#        if int(amount) > database_utils.fetch_balance(ctx.author.id):# and ctx.author.id != general_utils.bot_owner_id:
#            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "You can't pay what you dont have!"))
#            return
#            
#        recipient_name = await Bot.fetch_user(user_id)
#        recipient_name = recipient_name.name
#
#        await ctx.send(embed=discord.Embed(title=f"Confirmation: Do you want to send {'all of your money' if amount == 'all' else f'§{amount}'} to {recipient_name}?", colour=general_utils.Colours.yellow))
#        
#        check = lambda m: m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ["yes please", "yes", "ye", "yep", "yeah", "confirm", "affirmative", "true", "no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]
#
#        try:
#            msg = await Bot.wait_for('message', timeout=15.0, check=check)
#        except asyncio.TimeoutError:
#            await ctx.send("nevermind...")
#            return
#        
#        if msg.content.lower() in ["no", "nope", "no thanks", "nevermind", "denied", "false", "nevermind..."]:
#            await ctx.send(embed=general_utils.format_embed(ctx.author, discord.Embed(title=f"Okie, {random.choice(['nevermind!', 'aborted!'])}")))
#            return
#        cur_balance = database_utils.fetch_balance(ctx.author.id)
#        if amount == 'all':
#            delta = 0 - cur_balance
#        elif int(amount) > cur_balance:# and ctx.author.id != general_utils.bot_owner_id:
#            await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "You can't pay what you dont have!"))
#            return
#        else:
#            delta = 0 - int(amount)
#        #<:Simolean:769845739043684353> Simoleons
#        database_utils.alter_balance(ctx.author.id, delta)
#        database_utils.alter_balance(user_id, -delta)
#
#        paid_embed = general_utils.format_embed(ctx.author, discord.Embed(title=f"Paid {recipient_name} §{amount}."))
#        paid_embed.add_field(name=f"{ctx.author.name} Recieved:", value=f"{'+' if delta > -1 else ''}{delta} <:Simolean:769845739043684353> Simoleon{'s' if delta != 1 else ''}")
#        paid_embed.add_field(name=f"{recipient_name} Recieved:", value=f"{'+' if -delta > -1 else ''}{-delta} <:Simolean:769845739043684353> Simoleon{'s' if -delta != 1 else ''}")
#        
#        await ctx.send(embed=paid_embed)
#
#    Bot.add_command(_pay)