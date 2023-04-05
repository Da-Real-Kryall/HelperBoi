import requests, math, discord, asyncio, time, datetime
from utils import general_utils, database_utils
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands

class Geoforecast(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
        self.Bot.loop.create_task(self.event_loop())

    def make_forecast_table(self):
        data = (str(requests.get("https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt").content)[2:][:-1].replace("\\n", '\n'))

        days = data[484:].split('\n')[0].split("    ")

        data = [line[15:] for line in data[510:].split("\n")]
        data = [line.split("      ") for line in data][1:-1]
        data = [[round(float(data[i][g])*2) for i in range(len(data))] for g in range(3)]

        desc = f"""
`   (Graph is Kp index over time, one ██ = 3 hours.)        `
` ————————————————————————————————————————————————————————— `"""
        for g in range(18):
            desc += f"\n` {f'(G{(18-g)//2-4})' if g in [0, 2, 4, 6, 8]  else '    '} {str((18-g)//2) if g%2 == 0 else ' '} "
            for h in range(3):
                desc += '│' if h in [1,2] else '║'
                for i in [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]:
                    desc += (' ' if g not in [0, 2, 4, 6, 8] else '.') if 18-g > data[h][i] else '█'
            desc += '`'
        # three timestamps are midnight UTC for today, tomorrow and the day after tomorrow #--------- 9 chars leeway
        desc += f"""
`      0 ╚════════════════╪════════════════╪════════════════`
**`        │     {days[0]}     │     {days[1]}     │     {days[2]}     \u200b`**
**`        │                │                ┕`**<t:{int((datetime.utcnow() + timedelta(days=2)).timestamp())}:R>
**`        │                ┕`**<t:{int((datetime.utcnow() + timedelta(days=1)).timestamp())}:R>
**`        ┕`**<t:{int(datetime.utcnow().timestamp())}:R>"""
        return desc

    async def event_loop(self):
        while True:
            #activate every hour
            await asyncio.sleep(3600 - time.time() % 3600)
            data = (str(requests.get("https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt").content)[2:][:-1].replace("\\n", '\n'))
            data = [line[15:] for line in data[510:].split("\n")]
            data = [line.split("      ") for line in data][1:-1]
            data = sum(data, [])
            #data = max([float(data[i]) for i in range(len(data))]) # this errors, but when commented out it doesn't alter anything so I'll leave it commented for now. 

            if datetime.now().hour == 0:
                if data >= 5:
                    users = database_utils.fetch_users_by_setting("geoforecast", 1)
                    embed = discord.Embed(title=f"G{math.floor(data)-5} Storm(s) Warning:", description=self.make_forecast_table(), color="red")
                    for user in users:
                        user = self.Bot.get_user(user)
                        if user is not None:
                            await user.send(embed=embed)

    @app_commands.command(name="geoforecast", description="Get the Kp index forecast for the next 3 days.")
    async def geoforecast(self, interaction: discord.Interaction):
        embed = general_utils.Embed(interaction.user, "3 Day Geomagnetic Forecast:")
        desc = self.make_forecast_table()

        embed.description = desc

        embed.add_field(name="More Info:", value=f"""The Kp index is an indirect measure of the amount of solar wind reaching Earth.
A higher Kp index indicates greater geomagnetic activity in the Earth's magnetosphere, and is normally characterised by stronger auroras, more radio blackouts, and more power grid disturbances.
The Kp index is measured on a scale of 0 to 9, with anything above or equal to 5 being classed as a storm. 
*(A Kp of 5 denotes a G1 storm, with Kp 6 being G2, and so on.)*

A famous example of the effects of a G5 storm is the [1859 Carrington Event](https://en.wikipedia.org/wiki/Carrington_Event), which caused telegraph systems to fail across the world, and was the strongest geomagnetic storm ever recorded. We are overdue for another such event.""")
        await interaction.response.send_message(embed=embed, ephemeral=general_utils.is_ghost(interaction.user.id))

async def setup(Bot):
    await Bot.add_cog(Geoforecast(Bot))