import discord, textwrap, json, time
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"evaluate":{
        "aliases":["eval", "evaluate"],
        "syntax":"<code>",
        "usage":"Evalutes the given code (one line only), of which can be in an embed block. Only for the bot owner!",
        "category":"utility"
    }})

    @commands.is_owner()
    @commands.command(name="evaluate", aliases=["eval"])
    async def _evaluate(ctx, *, code=None):

        starttime = time.time()
 
        msg = await ctx.send(embed=discord.Embed(title='Evaluating code...', description='```Loading...```', colour=discord.Colour(general_utils.Colours.yellow)))

        if code.startswith('```py'):
            code = code[5:][:-3]
        env = dict(locals())
        env.update(globals())
        env.update({"Bot":Bot})
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


    Bot.add_command(_evaluate)
