import discord, requests, time
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"geoforecast":{
        "aliases":["geoforecast", "gf"],
        "syntax":"",
        "usage":"Returns some parsed info from a rest api showing the 3-day geomagnetic forecast, credit to the NOAA.",
        "category":"utility"
    }})
    @commands.command(name="geoforecast", aliases=["gf"])
    async def _geoforecast(ctx):
        stamplist = []
        datalist = []

        data = (str(requests.get("https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt").content)[2:][:-1].replace("\\n", '\n'))
        data = data[-296:]
        data = [line[15:] for line in data.split("\n")]

        for day in range(0,3):
          for line in range(0,8):
            datalist += [int(data[line][day*10])]

        for day in range(1,4): #[15, 25, 35]
          for sect in range(0,8):
            stamplist += [f"<t:{int(time.time()+((3)*sect+(1.5)+24*(day-1))*60*60)}:R>"]

        data_dict = {stamplist[g]:datalist[g] for g in range(24)}

        returnlist = []
        for item in data_dict.items():
          returnlist.append('`'+(" "*(20-(item[1]*2))+"<"*bool(item[1])+"="*(item[1]*2-1))+'`'+item[0])
        geo_embed = discord.Embed(title="3-day Geomagnetic Forecast:", description="` Storm Class (G<n>) `\n`  5 4 3 2 1         `\n`__|_|_|_|_|_________`\n"+("\n".join(returnlist))+"\n`T˜ˇ˜T˜ˇ˜T˜ˇ˜T˜ˇ˜T˜ˇ˜`\n`☹   8   6   4   2   `\n`      Kp Index      `", colour=general_utils.Colours.charcoal)
        geo_embed.add_field(name="Info:", value="The Kp index is a measure of the disturbances in the earth's magnetic field caused by solar winds. The range goes from 0, representing very little activity, to 9, being an intense geomagnetic storm; think Carrington event.")
        geo_embed = general_utils.format_embed(ctx.author, geo_embed)
        await ctx.send(embed=geo_embed)

    Bot.add_command(_geoforecast)