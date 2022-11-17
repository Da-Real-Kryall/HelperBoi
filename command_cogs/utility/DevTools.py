import discord, textwrap, json, time
from discord.ext import commands
from utils import general_utils

class DevTools(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DevTools cog loaded.")
    

    @commands.command(name="exec")
    @commands.is_owner()
    async def _exec(self, ctx, *, code=None):
        if code.startswith('```py'):
            code = code[5:][:-3]
        env = dict(locals())
        env.update(globals())
        env.update({"Bot":self.Bot})
        code = textwrap.indent(code, "  ")
        code = f"async def codefunc():\n{code}"
        try:
            exec(code, env)
            await env['codefunc']()
        except Exception as e:

            error_embed = discord.Embed(title=f"**{e.__class__.__name__} While Executing Code:**", description=f"```py\n{e.args[0] if hasattr(e, 'msg') == True else str(e)}```", colour=general_utils.Colours.red)

            if hasattr(e, 'lineno'): 
                error_embed.set_footer(text=', '.join([(f"{e.filename}" if hasattr(e, 'filename') == True else ""),(f"Line {e.lineno}" if hasattr(e, 'lineno') == True else "")]))
            
            if '\'await\' expression' not in str(e):
                await ctx.send(embed=error_embed)



    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, code=None):

        starttime = time.time()
 
        msg = await ctx.send(embed=discord.Embed(title='Evaluating code...', description='```Loading...```', colour=discord.Colour(general_utils.Colours.yellow)))

        if code.startswith('```py'):
            code = code[5:][:-3]
        env = dict(locals())
        env.update(globals())
        env.update({"Bot":self.Bot})
        code = textwrap.indent(code, "  ")
        code = f"async def codefunc():\n return {code}"

        try:
            exec(code, env)
            result = await env['codefunc']()
            
            try:
                result = json.dumps(result, indent=4)
            except TypeError:
                result = str(result)
            
            
            result_embed = discord.Embed(title='Success!', description="```py\n"+str(result[:2035]+('...' if len(result) > 2035 else ''))+"\n```", colour=general_utils.Colours.green)
            
            if len(result) > 2035:
                result_embed.add_field(name="Note:", value=f"Response was {len(result)-2035} chars too long, result was trimmed and the rest printed to console.")
                print(result)

            result_embed.set_footer(text=f"{round(time.time()-starttime, 2)}s")

            await msg.edit(embed=result_embed)

        except Exception as e:

            error_embed = discord.Embed(title=f"**{e.__class__.__name__} While Evaluating Code:**", description=f"```py\n{e.args[0] if hasattr(e, 'msg') == True else str(e)}```", colour=general_utils.Colours.red)

            if hasattr(e, 'lineno'): 
                error_embed.set_footer(text=', '.join([(f"{e.filename}" if hasattr(e, 'filename') == True else ""),(f"Char {e.offset}" if hasattr(e, 'offset') == True else "")]))
            
            if '\'await\' expression' not in str(e): await msg.edit(embed=error_embed)



async def setup(Bot):
    await Bot.add_cog(DevTools(Bot))
