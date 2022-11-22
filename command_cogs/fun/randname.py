import discord, random, json
from discord.ext import commands
from discord import app_commands
from utils import general_utils

compatible_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']
min_length = 3
max_length = 9

with open("Resources/json/randname_weighting.json") as file:
    weighting = json.load(file)

def generate_embed(user: discord.User, count: int) -> discord.Embed:
    namelist = []
    for _ in range(count):
        #markov chains implementation from strings

        #final word!
        result = ''
        #calculate first character

        choicelist = []

        for char in compatible_letters[:-1]:
            num_occurances = weighting['-'][char]
            if num_occurances != 0:
                choicelist += [char]*num_occurances

        result += random.choice(choicelist)

        for g in range(1, 100):
            choicelist = []
            if len(result) < min_length:
                for char in compatible_letters[:-1]:
                    num_occurances = weighting[result[-1]][char]
                    if num_occurances != 0:
                        choicelist += [char]*num_occurances
                    #print(choicelist)

            elif len(result) > max_length:
                for char in compatible_letters:
                    num_occurances = weighting[result[-1]][char]
                    if num_occurances != 0:
                        if char == '-':
                            choicelist += [char]*(num_occurances*(len(result)-max_length)*2)
                        else:
                            choicelist += [char]*num_occurances
                    #print(choicelist)

            else:
                for char in compatible_letters:
                    num_occurances = weighting[result[-1]][char]
                    if num_occurances != 0:
                        choicelist += [char]*num_occurances
                    #print(choicelist)

            nextchar = random.choice(choicelist)
            result += nextchar

            if result[-1] == '-':
                #print(choicelist)
                namelist += [result[:-1].capitalize()]
                break
            
    embed = general_utils.Embed(author=user, title='\n'.join(namelist))
    return embed

class Controller(discord.ui.View):
    def __init__(self, count):
        super().__init__()
        self.add_item(discord.ui.Button(label=f"Reroll", custom_id=f"rn.{count}", style=discord.ButtonStyle.blurple))

class RandName(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("RandName cog loaded.")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data['custom_id'].split('.')[0] == 'rn':
            await interaction.response.defer()
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=generate_embed(interaction.user, int(interaction.data['custom_id'].split('.')[1])), view=Controller(count=int(interaction.data['custom_id'].split('.')[1])))
    
    @app_commands.command(name="randname", description="Random name generator 4.0! uses markov chains to generate name, trained a british name data set.")
    async def _randname(self, interaction: discord.Interaction, count: app_commands.Range[int, 1, 10]=1) -> None:
        embed = generate_embed(interaction.user, count)


            #@discord.ui.button(label="Reroll", style=discord.ButtonStyle.blurple, custom_id="rn."+str(count))
            #async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
            #    pass#await interaction.response.edit_message(embed=generate_embed(interaction.user, count), view=self)

        await interaction.response.send_message(embed=embed, view=Controller(count))
                    
async def setup(Bot):
    await Bot.add_cog(RandName(Bot))
