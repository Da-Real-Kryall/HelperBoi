import discord, random, json
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    compatible_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']
    min_length = 3
    max_length = 9

    with open("Recources/json/randname_weighting.json") as file:
        weighting = json.load(file)

    Bot.command_info.update({"randname":{
        "aliases":["randname"],
        "syntax":"[count]",
        "usage":"Random name generator 4.0! uses markov chains to generate name, trained a british name data set. Please pick a count below or equal 10.",
        "category":"fun"
    }})
    @commands.command(name="randname")
    async def _randname(ctx, count="1"):

        if general_utils.represents_int(count) == False:
            await ctx.send(embed=general_utils.error_embed(False, "Please pick a valid positive number for count below or equal to 10, generating names is hard!"))
            return

        #these are split because it errors i think if they are combined
        if int(count) > 10 or int(count) < 1:
            await ctx.send(embed=general_utils.error_embed(False, "Please pick a valid positive number for count below or equal to 10, generating names is hard!"))
            return
        
        count = int(count)

        namelist = []
        for iteration in range(count):
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
        
        embed = general_utils.format_embed(ctx.author, discord.Embed(title='\n'.join(namelist)))
        await ctx.send(embed=embed)
                    

    Bot.add_command(_randname)
