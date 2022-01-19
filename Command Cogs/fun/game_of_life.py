import discord, numpy, io, tempfile, time, os, random
from PIL import Image
from discord.ext import commands
from utils import general_utils

def setup(Bot):

    Bot.command_info.update({"game_of_life":{
        "aliases":["game_of_life", "gol"],
        "syntax":"[board width]x[board height] [num iterations]",
        "usage":"Runs a conway's game of life simulation. board size is given as `<width>x<height>`, is capped at 80x80 and defaults to `50x50`. num iterations is given as a normal positive integer also capped at 80, and defaults to 30.",
        "category":"fun"
    }})
    @commands.command(name="game_of_life", aliases=["gol"])
    async def _game_of_life(ctx, board_size="50x50", num_iterations="30"):
        async with ctx.typing(): #i could likely shorten this.
            if '*' in board_size:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "The board size you gave is invalid, make sure to give `<width>x<height>` and not `<width>*<height>`."))
                return
            elif 'x' not in board_size:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "The board size you gave is invalid, make sure you give it as `<width>x<height>` without spaces between x and width/height."))
                return
            size = board_size.split('x')
            if len(size) != 2:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "The board size you gave is invalid, make sure to give it as `<width>x<height>`.\n(eg `20x30`)"))
                return
            elif sum([general_utils.represents_int(x) for x in size]) != 2:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "The board size you gave is invalid, make sure to make both width and height valid integers."))
                return
            elif sum([int(x)>0 for x in size])!=2:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "The board size you gave is invalid, make sure to make both width and height positive integers."))
                return
            elif sum([int(x)<=50 for x in size])!=2:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "The board size you gave is larger than the maximum of 50x50."))
                return
            size = (int(size[0]),int(size[1]))
            if not general_utils.represents_int(num_iterations):
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Your given number of iterations was not a valid integer, please ensure it is one."))
                return
            elif int(num_iterations) < 0:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Your given number of iterations was negative, be sure to make the number of iterations a positive integer."))
                return
            elif int(num_iterations) > 80:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, False, "Your given number of iterations should be less than or equal to 80."))
                return
            numiters = int(num_iterations)

            colours = [(0, 0, 0), (0xFF, 0xFF, 0xFF), ]
            bordersize = max([int(max(size)/9), 8])
            div_bordersize = int(bordersize/2)
            array = numpy.random.randint(2, size=size)#[[random.randint(0,1) for g in range(size[0])]]*size[1]
            array = numpy.array(array)
            im = Image.new("P", (size[0]+bordersize, size[1]+bordersize), (45, 45, 50))#(46, 45, 43))
            for x in range(size[1]):
                for y in range(size[0]):
                    im.putpixel((y+div_bordersize, x+div_bordersize), colours[int(array[y][x])])
            im = im.resize((int((size[0]+bordersize)*4),int((size[1]+bordersize)*4)))

            images = [im]*2
            adjacents = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1),]

            for g in range(numiters):

                im = Image.new("P", (size[0]+bordersize, size[1]+bordersize), (45, 45, 50))
                newarray = numpy.zeros(size)
                
                for x in range(size[1]):
                    for y in range(size[0]):
                        newpixel = [0,0,array[y][x],1,0,0,0,0,0][sum([int(array[(y+_y)%size[0]][(x+_x)%size[1]]) for _y, _x in adjacents])]
                        newarray[y][x] = newpixel
                        im.putpixel((y+div_bordersize, x+div_bordersize), colours[int(newarray[y][x])])

                array = newarray
                im = im.resize((int((size[0]+bordersize)*4),int((size[1]+bordersize)*4)))
                images += [im]*2

            tmp_file=tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
            images[0].save(tmp_file.name, save_all=True, append_images=images[1:], optimize=False, duration=(numiters+1)*2,loop=0, format="gif")
            tmp_file.close()

            embed = discord.Embed(title='Finished Simulation:')
            embed = general_utils.format_embed(ctx.author, embed, "none")
            temp_file = discord.File(tmp_file.name, filename = "gol.gif")
            embed.set_image(url=f"attachment://gol.gif")
            try:
                await ctx.send(file=temp_file,embed=embed)
            except discord.errors.HTTPException:
                await ctx.send(embed=general_utils.error_embed(Bot, ctx, True, "The final simulation seems to be too large to send, try specifying a lesser iteration number or smaller board."))
            time.sleep(0.4)
            os.unlink(tmp_file.name)
    Bot.add_command(_game_of_life)