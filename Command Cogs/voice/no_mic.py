import random
from discord.ext import commands

def setup(Bot):

    Bot.command_info.update({"no_mic":{
        "aliases":["no_mic", "nm"],
        "syntax":"",
        "usage":"Will toggle relaying the author's messages sent from the current text channel into the author's voice channel, using a randomized generated voice.\nIntended for when one cannot use their microphone/does not want to use their microphone.",
        "category":"voice"
    }})
    @commands.guild_only()
    @commands.command(name="no_mic", aliases=["nm"])
    async def _no_mic(ctx):

        tld_list = [
            "com.au",
            "co.uk",
            "com",
            "ca",
            "co.in",
            "ie",
            "co.za",
            "fr",
            "com.br",
            "pt",
            "com.mx",
            "es"
        ]

        if ctx.guild.id not in Bot.current_nm_sessions:

            channel = ctx.author.voice.channel
            vc = await channel.connect()

            Bot.current_nm_sessions.update({
                int(ctx.guild.id): {
                    "voice_client": vc,
                    "users": {
                        int(ctx.author.id): random.choice(tld_list)
                    }
                }
            })
            await ctx.send("You have been added to the session.")
        else:
            if ctx.author.id not in Bot.current_nm_sessions[ctx.guild.id]["users"]:
                Bot.current_nm_sessions[ctx.guild.id]["users"].update({
                    int(ctx.author.id): random.choice(tld_list)
                })
            else:
                Bot.current_nm_sessions[ctx.guild.id]["users"].pop(ctx.author.id)
                await ctx.send("You have now been removed from the session.")
                if len(Bot.current_nm_sessions[ctx.guild.id]["users"]) == 0:
                    await Bot.current_nm_sessions[ctx.guild.id]["voice_client"].disconnect()
                    Bot.current_nm_sessions.pop(ctx.guild.id)
                    await ctx.send("Ended the session in this channel because there were no active users. Have a nice day!")

    Bot.add_command(_no_mic)