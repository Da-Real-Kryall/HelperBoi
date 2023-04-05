import discord, textwrap, json, time
from discord.ext import commands
from discord import app_commands
from utils import general_utils, database_utils

def suggest_embed_modifier(embed: discord.Embed, scroll_index: int, interaction: discord.Interaction):
    identifier = interaction.data["custom_id"].split(".")[0]
    print(identifier)
    submissions = database_utils.fetch_submissions(identifier)

    embed.set_footer(text=f"{identifier.capitalize()} {min(scroll_index + 1, len(submissions))} of {len(submissions)}")
    
    embed.clear_fields()
    embed.description = ""
    for index, submission in enumerate(submissions):
        embed.description += f"` {'>' if index == scroll_index else ' '} ` **[**<t:{submission[3]}:R>**]** - \"{submission[2][:16]+('...' if len(submission[2]) > 16 else '')}\"\n"
        #embed.add_field(name="Message:", value=submission[2], inline=False)
    
    return embed

class DevTools(commands.Cog):
    def __init__(self, Bot: commands.Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DevTools cog loaded.")

    @app_commands.command(name="reload", description="Reloads a cog.")
    @app_commands.guilds(discord.Object(id=747834673685594182))
    @general_utils.is_owner()
    async def _reload(self, interaction: discord.Interaction, cog: str) -> None:
        try:
            await self.Bot.reload_extension("command_cogs."+cog)
            await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title="Cog reloaded successfully.", colour="green"), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message=f"The following error occurred while reloading the cog:\n```py\n{e}\n```"), ephemeral=True)
        
    @app_commands.command(name="sync", description="Syncs slash commands.")
    @general_utils.is_owner()
    @app_commands.guilds(discord.Object(id=747834673685594182))
    async def _sync(self, interaction: discord.Interaction):
        if interaction.user.id != 479963507631194133:
            return await interaction.response.send_message(embed=general_utils.error_embed(author=interaction.user, message="You are not the owner of this bot.", apologise=False), ephemeral=True)
        fmt = await self.Bot.tree.sync()
        await interaction.response.send_message(embed=general_utils.Embed(author=interaction.user, title=f"Synced {len(fmt)} commands globally.", colour="green"))

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

    


    @app_commands.command(name="submissions", description="Recalls and displays either bugreports or suggestions in a menu.")
    @app_commands.choices(
        submission_type=[
            app_commands.Choice(name="Bugreports", value="bug"),
            app_commands.Choice(name="Suggestions", value="suggestion")
        ]
    )
    # ensure the command author is the bot owner
    @general_utils.is_owner()
    async def _submissions(self, interaction: discord.Interaction, submission_type: str):
        print(submission_type)
        await interaction.response.defer()
        submissions = database_utils.fetch_submissions(submission_type)
        print(submissions, len(submissions))
        if len(submissions) == 0:
            embed = general_utils.Embed(author=interaction.user, title=f"No {submission_type}s!", description="Nobody has given you any feedback. :(")
            await interaction.followup.send(embed=embed)
            return

        embed = general_utils.Embed(author=interaction.user, title={"bug": "Bug Reports:", "suggestion": "Suggestions:"}[submission_type], description="")
        interaction.data.update({"custom_id": f"{submission_type}.0"})
        embed = suggest_embed_modifier(embed, 0, interaction)

        await interaction.followup.send(embed=embed, view=general_utils.Controller(submission_type, 0, len(submissions)))

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # suggestions
        if "custom_id" in interaction.data.keys():
            if interaction.data["custom_id"].split(".")[0] == "suggestion":
                def delete_suggestion(scroll_index: int):
                    suggestions = database_utils.fetch_submissions("suggestion")
                    id = suggestions[scroll_index][0]
                    database_utils.remove_submission(id, "suggestion")
                    return max(scroll_index-1, 0)
                functions = general_utils.make_functions_dict("suggestion", suggest_embed_modifier, delete_suggestion)
                await general_utils.interaction_listener_generator("suggestion", functions)(interaction)

            # bugreports
            if interaction.data["custom_id"].split(".")[0] == "bug":
                def delete_bug(scroll_index: int):
                    suggestions = database_utils.fetch_submissions("bug")
                    id = suggestions[scroll_index][0]
                    database_utils.remove_submission(id, "bug")
                    return max(scroll_index-1, 0)
                functions = general_utils.make_functions_dict("bug", suggest_embed_modifier, delete_bug)
                await general_utils.interaction_listener_generator("bug", functions)(interaction)
            

async def setup(Bot):
    await Bot.add_cog(DevTools(Bot))
