import discord, time, os, requests, asyncio, threading, datetime
from discord.ext import commands
from discord import app_commands
from utils import database_utils, general_utils
# data is ("reminder", timestamp, (id, user_id, message, timestamp, channel_id))
async def thread_function(Bot, data):
    if data[0] == "reminder":
        await asyncio.sleep(max(0, data[1] - time.time()))
        # send reminder
        user = Bot.get_user(data[2][1])
        if user == None:
            user = await Bot.fetch_user(data[2][1])

        channel = await Bot.fetch_channel(data[2][4])
        await channel.send(f"<@!{data[2][1]}>, reminder:", embed=general_utils.Embed(author=user, title=data[2][2]))
        # remove reminder from database
        database_utils.remove_reminders([data[2][0]])
    elif data[0] == "geoforecast":
        await asyncio.sleep(max(0, data[1] - time.time()))
        # send warning message
        pass

async def event_loop(Bot):
    Bot.event_cache = []# (type, time, data)
    data = database_utils.fetch_reminders() # [(id, user_id, message, timestamp, channel_id)]
    for reminder in data:
        # if the reminder occurs today, add it to the cache
        if reminder[3] - time.time() < 86400:
            # if it occurs in the next hour, spawn a thread to send it
            if reminder[3] - time.time() < 3600:
                Bot.loop.create_task(thread_function(Bot, ("reminder", reminder[3], reminder)))
                #await _thread_function(Bot, ("reminder", reminder[3], reminder))
                #threading.Thread(target=thread_function, args=(Bot, ("reminder", reminder[3], reminder))).start()
            else:
                Bot.event_cache.append(("reminder", reminder[3], reminder))

    while True:
        #activate every hour
        await asyncio.sleep(3600 - time.time() % 3600)

        if datetime.datetime.now().hour == 0:
            Bot.event_cache = []
            data = database_utils.fetch_reminders() # [(id, user_id, message, timestamp, channel_id)]
            for reminder in data:
                # if the reminder occurs today, add it to the cache
                if reminder[3] - time.time() < 86400:
                    # if it occurs in the next hour, spawn a thread to send it
                    if reminder[3] - time.time() < 3600:
                        Bot.loop.create_task(thread_function(Bot, ("reminder", reminder[3], reminder)))
                        #await _thread_function(Bot, ("reminder", reminder[3], reminder))
                    else:
                        Bot.event_cache.append(("reminder", reminder[3], reminder))
            #add geoforecast events to the cache
            pass
        else:
            for event in Bot.event_cache:
                if event[1] - time.time() < 3600:
                    Bot.loop.create_task(thread_function(Bot, event))
                    #await _thread_function(Bot, ("reminder", reminder[3], reminder))
                    #threading.Thread(target=thread_function, args=(Bot, event)).start()
                    Bot.event_cache.remove(event)

async def setup(Bot):
    Bot.thread_function = thread_function
    Bot.loop.create_task(event_loop(Bot))
    #threading.Thread(target=event_loop, args=(Bot,)).start()
