import os, json, random, re
from utils import database_utils, general_utils
def setup(Bot):

    #a toggleable light swear filter

    with open(os.getcwd()+"/Recources/json/censoring_data.json") as file:
        censor_json = json.loads(file.read())

    @Bot.listen()
    async def on_message(message):
        if message.author.bot == False and message.guild != None:
            if database_utils.fetch_setting("servers", message.guild.id, "censoring") == 1:
                censor_ranges = [] #(start_index, end_index) 
                content = list(message.content)
                reference_content = message.content #content with swapped chars etc, same length as normal content!

                for char_from, char_to in censor_json['swapped_characters'].items():
                    reference_content = reference_content.replace(char_from, char_to)
                
                expressions = []
                for word in censor_json['words_to_filter']:
                    expression = '(?i)'
                    for char in word[:-1]:
                        expression += rf"{char}[{char}\u200b]*?"
                    expression += f'{word[-1]}+'
                    expressions += [expression]
                #print(expressions)

                for expression in expressions:
                    matches = re.finditer(expression, reference_content)
                    for match in matches:
                        censor_ranges += [match.span()]
                
                for censor_range in censor_ranges:
                    for index in range(censor_range[0], censor_range[1]):
                        content[index] = random.choice(['#', '@', '%', '$', '&', '!', ':', '?', '|'])#█'░'#'[', ']', '{', '}', '(', ')', '/',, '\\\\'
                
                content = ''.join(content)

                if content != message.content:
                    await message.delete()
                    await general_utils.send_via_webhook(message, Bot, content, message.author.name, message.author.avatar_url)