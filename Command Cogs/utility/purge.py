import asyncio
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"purge":{
        "aliases":["purge", "bulkdelete"],
        "syntax":"<num messages>",
        "usage":"For clearing channels, will delete the last <num messages> messages from the channel the command was sent in. Requires the manage messages permission, and the <num messages> must be below 101.",
        "category":"utility"
    }})

    @commands.has_permissions(manage_messages=True)
    @commands.command(name="purge", aliases=["bulkdelete"])
    async def _purge(ctx, num_messages):
        if general_utils.represents_int(num_messages) == False or (int(num_messages) > 100):
            await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "Please give a valid integer below 101."))
            return

        await ctx.channel.purge(limit=int(num_messages))

        msg = await ctx.send(f"Deleted {num_messages} messages.")
        await asyncio.sleep(100)
        try:
            await msg.delete()
        except:
            pass

    Bot.add_command(_purge)
