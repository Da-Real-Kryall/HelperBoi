import discord, textwrap
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"execute":{
        "aliases":["exec", "execute"],
        "syntax":"<code>",
        "usage":"Executes the given code, of which can be in an embed block. only for the bot owner!",
        "category":"utility"
    }})

    @commands.is_owner()
    @commands.command(name="execute", aliases=["exec"])
    async def _execute(ctx, *, code=None):
        if code.startswith('```py'):
            code = code[5:][:-3]
        env = dict(locals())
        env.update(globals())
        env.update({"Bot":Bot})
        code = textwrap.indent(code, "  ")
        code = f"async def codefunc():\n{code}"
        try:
            exec(code, env)
            await env['codefunc']()
        except Exception as e:

            error_embed = discord.Embed(title=f"**{e.__class__.__name__} While Executing Code:**", description=f"```py\n{e.args[0] if hasattr(e, 'msg') == True else str(e)}```", colour=general_utils.Colours.red)

            if hasattr(e, 'lineno'): 
                error_embed.set_footer(text=', '.join([(f"{e.filename}" if hasattr(e, 'filename') == True else ""),(f"Line {e.lineno}" if hasattr(e, 'lineno') == True else "")]))
            
            if '\'await\' expression' not in str(e): await ctx.send(embed=error_embed)

        
        #dontexcept = True
        #try:
        #    compiled_code = compile(code, "<string>", mode="exec", flags=__import__('ast').PyCF_ALLOW_TOP_LEVEL_AWAIT)
        #except Exception as e:
        #    kind, exc_obj, exc_tb = sys.exc_info()
        #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #    if '\'await\' expression' not in str(e):
        #        dontexcept = False
        #        await ctx.send(embed=discord.Embed(title="**"+str(kind)[8:][:-2]+f" While Executing Code:**\n{fname}, Line {e.lineno}", description="```py\n"+str(e)+"```", colour=discord.Colour(0xea1510)))
        #try:
        #    await eval(compiled_code)
        #except Exception as e:
        #    kind, exc_obj, exc_tb = sys.exc_info()
        #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #    if '\'await\' expression' not in str(e) and dontexcept == True:
        #        await ctx.send(embed=discord.Embed(title="**"+str(kind)[8:][:-2]+f" While Executing Code:**\n{fname}, Line {exc_tb.tb_lineno}", description="```py\n"+str(e)+"```", colour=discord.Colour(0xea1510)))


    Bot.add_command(_execute)
