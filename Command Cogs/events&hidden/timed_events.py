#active events that trigger on certain timestamps

#passive events trigger if something happens after x hours (usually for requesting a kind of data)

from utils import database_utils, general_utils
import time, asyncio, os, discord, requests
from datetime import datetime

def setup(Bot):
    async def _add_reminder(content, delta, message):
        timestamp = int(time.time()+delta)
        ID = database_utils.add_reminder(content, timestamp, message.author.id, message.guild.id, message.channel.id)
        datacache['active']['reminders']['saved'] += [(ID, content, timestamp, message.author.id, message.guild.id, message.channel.id)]
        if delta < 3600:
            await threadfunc((ID, content, timestamp, message.author.id, message.guild.id, message.channel.id))
    Bot.add_reminder = _add_reminder

    #passive updates, data thhat refreshes when its requested after x hours
    datacache = {#cooldown is in hours, this isnt json as itl be storing other data types not easily encodable to json
        "passive": {
            "cooltop": {
                "value": None,
                "cooldown": 12,
                "timestamp": int(time.time())
            },
            "baltop": {
                "value": None,
                "cooldown": 12,
                "timestamp": int(time.time()) #last use
            }
        },
        "active": {
            "reminders": {
                "saved": [],#(ID, content, timestamp, author_id, guild_id, channel_id)
                "doing": []
            }, 
            "gf_alert": [] #list of userids
        }
    }
    async def threadfunc(reminder):
        datacache['active']['reminders']['saved'] += [reminder[0]] #add id to list of reminders that have a threadfunc active
        guild = Bot.get_guild(reminder[4])
        channel = guild.get_channel(reminder[5])
        embed = discord.Embed(title=reminder[1], colour=general_utils.Colours.main) #description=f"(Set <t:{reminder[2]}:R>)", #add "set at <date>" description on reminder embed

        await asyncio.sleep(int(reminder[2]-time.time()))
        await channel.send(f"<@!{reminder[3]}>, reminder:", embed=embed)

        datacache['active']['reminders']['saved'].remove(reminder)

        database_utils.remove_reminders([reminder[0]])
        datacache['active']['reminders']['saved'].remove(reminder[0])

    async def _request_global(value: str):
        if value not in ["cooltop", "baltop"]:
            raise KeyError("the only currently valid args are cooltop and baltop for value.")
        if value == 'cooltop':
            if int(time.time()) > datacache['passive'][value]['timestamp']:
                userlist = []
                for userid in [int(filename.name[:-3]) for filename in os.scandir("Databases/users")]:
                    if database_utils.fetch_setting("users", userid, "economy_invisibility") == False:
                        try:
                            user = await Bot.fetch_user(userid)
                        except:
                            user = None
                        if user != None:
                            username = user.name
                        else:
                            username = "Unknown :("
                        userlist += [[f"{username[:24]}{' '*(24-len(username))}", *database_utils.fetch_coolness(userid)]] 
                userlist.sort(key = lambda l: l[1])
                userlist = list(reversed(userlist))
                userlist = userlist[:10]
                datacache['passive'][value]['timestamp'] = int(time.time()+datacache['passive'][value]['cooldown']*60*60)
                datacache['passive'][value]['value'] = userlist
                return userlist
            else:
                return datacache['passive'][value]['value']
        elif value == 'baltop':
            if int(time.time()) > datacache['passive'][value]['timestamp']:
                userlist = []
                for userid in [int(filename.name[:-3]) for filename in os.scandir("Databases/users")]:
                    if database_utils.fetch_setting("users", userid, "economy_invisibility") == False:
                        try:
                            user = await Bot.fetch_user(userid)
                        except:
                            user = None
                        if user != None:
                            username = user.name
                        else:
                            username = "Unknown :("
                        userlist += [[f"{username[:24]}{' '*(24-len(username))}", database_utils.fetch_balance(userid)]] # *detabase...{user.discriminator}
                userlist.sort(key = lambda l: l[1])
                userlist = list(reversed(userlist))
                userlist = userlist[:10]
                datacache['passive'][value]['timestamp'] = int(time.time()+datacache['passive'][value]['cooldown']*60*60)
                datacache['passive'][value]['value'] = userlist
                return userlist
            else:
                return datacache['passive'][value]['value']
            userlist = []
    Bot.request_global = _request_global
    #active updates, to implement geoforecast and reminders
    @Bot.listen()
    async def on_connect():
        await asyncio.sleep(1)
        datacache["active"]["gf_alert"] = [user.id for user in Bot.users if database_utils.fetch_setting("users", user.id, "geoforecast_alert") == 1]
        datacache['active']['reminders']['saved'] = [res for res in database_utils.fetch_reminders()] #reminders that should go off within the hour or should have gone off before now
        while True:
            hour = datetime.today().hour
            if hour == 20: #noon utc
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

                data_dict = {stamplist[g]:datalist[g]-4 for g in range(24) if datalist[g] > 4}

                if len(data_dict) != 0:
                    for userid in datacache['active']['gf_alert']:
                        try:
                            user = Bot.get_user(userid)
                            embed = general_utils.format_embed(user, discord.Embed(title="Warning, Geomagnetic storms will be occuring at:", description="\n".join([f"{key} (G{value})" for key, value in data_dict.items()])), "red")
                            await (Bot.get_user(userid)).send(embed=embed)
                        except discord.errors.HTTPException: #user does not have a mutual server with bot
                            pass
            
            #do reminders
            for reminder in datacache['active']['reminders']['saved']:
                if reminder[0] not in datacache['active']['reminders']['saved']:
                    await threadfunc(reminder)

            await asyncio.sleep(60*60) #every hour