from typing import Container
import discord, scpscraper, random, string, django.utils.timezone, datetime
from discord.ext import commands
from utils import general_utils



def setup(Bot):

    Bot.command_info.update({"scp":{
        "aliases":["scp"],
        "syntax":"[scp number]",
        "usage":"Scrapes the scp website database, and returns info about a random scp or the one of the id given.\n(Be wary, this is *veerryy slooww*)\n(Also powered by the scpscraper api)",
        "category":"fun"
    }})
    @commands.command(name="scp")
    async def _scp(ctx, number=''):
        do_error = False
        if general_utils.represents_int(number):
            if int(number) > 6100 or int(number) < 1:
                do_error = True
        elif number != '':
            do_error = True

        if do_error:
            error_embed = general_utils.error_embed(True, "You need to give an integer in the range of 1-6100 or leave the args blank!")
            await ctx.send(embed=error_embed)
            return


        if number == '':
            number = random.randint(2, 6100)
        else:
            number = int(number)

        scp_embed = discord.Embed(colour=general_utils.Colours.yellow, title="Loading...", description="Loading...\n_ _")

        msg = await ctx.send(embed=scp_embed)


        async with ctx.typing():
            name = scpscraper.get_scp_name(int(number))
            if str(name) == "None":
                name = "Unknown"

            scp_num = f"SCP-{'000'[:((3-len(str(number))) if (3-len(str(number))) > 0 else 0)]}{number}"

            scp_embed = discord.Embed(colour=general_utils.Colours.yellow, title=f"{scp_num}: {name}", description="Loading...\n_ _")

            await msg.edit(embed=scp_embed)

            try:
                info = scpscraper.get_scp(int(number))
            except TypeError:
                scp_embed.title = f"{'Sorry!' if random.randint(1, 15) != 1 else 'Sorey!'}, it seems {scp_num} does not exist!"
                scp_embed = general_utils.format_embed(ctx.author, scp_embed, "red")
                await msg.edit(embed=scp_embed)
                return
            
            if "content" not in info.keys() and "image" not in info.keys():
                scp_embed.title = f"{'Sorry!' if random.randint(1, 15) != 1 else 'Sorey!'}, it seems {scp_num} does not exist!"
                scp_embed.colour = general_utils.Colours.red
                scp_embed = general_utils.format_embed(ctx.author, scp_embed)
                await msg.edit(embed=scp_embed)
                return

            #define attributes seperately so there isnt a huge one liner

            object_class = "Unknown"
            if "content" in info.keys():
                if info["content"] != None:
                    if "Object Class" in info["content"].keys():
                        if info["content"]["Object Class"] != None:
                            object_class = info["content"]["Object Class"]

            image_src = None
            image_caption = None
            if "image" in info.keys():
                if info["image"] != None:
                    if "src" in info["image"].keys():
                        if info["image"]["src"] != None:
                            image_src = info["image"]["src"]
                    if "caption" in info["image"].keys():
                        if info["image"]["caption"] != None:
                            image_caption = info["image"]["caption"]

            scp_embed = discord.Embed(colour=general_utils.Colours.yellow, title=f"{scp_num}: {name}", description=f"***Object Class:*** *{object_class}*\n"+(f"***Image caption:*** *{image_caption}*" if image_caption != None else ""))

            if image_src != None:
                scp_embed.set_image(url=image_src)

            await msg.edit(embed=scp_embed)

            max_chars = 1024

            if "content" in info.keys():
                if info["content"] != None:
                    if "Special Containment Procedures" in info["content"].keys():
                        if info["content"]["Special Containment Procedures"] != None:
                            containment_procedures = info["content"]["Special Containment Procedures"]
                            if len(containment_procedures) > max_chars:
                                containment_procedures = containment_procedures[:max_chars-3]+"..."
                                scp_embed.add_field(name="Special Containment Procedures:",        value=containment_procedures, inline=False)
                                await msg.edit(embed=scp_embed)
                    if "Description" in info["content"].keys():
                        if info["content"]["Description"] != None:
                            description = info["content"]["Description"]
                            if len(description) > max_chars:
                                description = description[:max_chars-3]+"..."
                            scp_embed.add_field(name="Description:", value=description, inline=False)
                            await msg.edit(embed=scp_embed)

            url = f"https://scp-wiki.wikidot.com/scp-{'000'[:((3-len(str(number))) if (3-len(str(number))) > 0 else 0)]}{number}"

            scp_embed.url = url
            scp_embed.colour = general_utils.Colours.main
            scp_embed = general_utils.format_embed(ctx.author, scp_embed)
            
            await msg.edit(embed=scp_embed)

    Bot.add_command(_scp)
