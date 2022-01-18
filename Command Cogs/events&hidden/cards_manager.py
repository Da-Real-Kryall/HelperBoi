import random, discord, asyncio
from utils import general_utils, database_utils

def setup(Bot):
    
    class cah():
        """
        The place where i chuck all the cah functions and data so i dont clutter my namespace across files.
        """
        def __init__(self):
            self.current_cah_sessions = {}
            self.current_active_players = {}

        class errors:
            class AlreadyInGame(Exception):
                """
                Raised when a user already playing a cah game attempts to create a new game before leaving.
                """
                pass
            class NotInAGame(Exception):
                """
                Raised when a user not currently in a cah game attempts to make an action that requires them to be in a game.
                """
                pass
            class NotValidKey(Exception):
                """
                Raised when a game key is used that doesnt correspond to any currently active cah games.
                """
                pass
            class NotGameOwner(Exception):
                """
                Raised when a non-owner attempts to make an owner-only action concerning a Cards-Against-Humanity game.
                """
                pass
            class NotEnoughPlayers(Exception):
                """
                Raised when someone attempts to perform an action requiring more players than are currently in their cah game.
                """
                pass
            class PlayerNotMessagable(Exception):
                """
                Raised when a user for whatever reason has disabled direct messaging in a way that also prevents the bot from sending them DMs.
                """
                pass

            
        def create_cah_session(self, owner_id:int) -> str:
            """
            Creates a new cah game with the given user id as its owner, raises AlreadyInGameError if the user is already running/in a cah game.
            """
            if owner_id in self.current_active_players:
                raise self.errors.AlreadyInGame("Player is already part of another game!")
            else:
                key = "ABCDEFGH"
                lim = 262143
                GameKey = ''.join([key[int(x)] for x in str(oct(random.randint(0, lim)))[2:].zfill(6)])
                while GameKey in self.current_cah_sessions:
                    GameKey = ''.join([key[int(x)] for x in str(oct(random.randint(0, lim)))[2:].zfill(6)])

                cards = [card[1] for card in database_utils.fetch_cards("white", 7)]

                self.current_active_players.update({int(owner_id): GameKey})
                self.current_cah_sessions.update({
                    GameKey: {
                        "owner": int(owner_id),
                        "state": "starting",
                        "members": {
                            int(owner_id): {
                                "cards": cards,
                                "points": 0
                            }
                        }
                    }
                })
            return GameKey
        
        async def join_cah_game(self, userid: int, GameKey):
            if int(userid) in self.current_active_players:
                raise self.errors.AlreadyInGame("Player is already part of another game!")
            cards = [card[1] for card in database_utils.fetch_cards("white", 7)]

            joineduser = Bot.get_user(int(userid))
            try:
                await joineduser.send(embed=discord.Embed(title=f"You have joined game `{GameKey}`, current leaderboard:"))
            except:
                raise self.errors.PlayerNotMessagable("couldnt send them a dm")

            for member in self.current_cah_sessions[GameKey]["members"]:
                await Bot.get_user(member).send(embed=discord.Embed(title=f"{joineduser} just joined!", colour=general_utils.Colours.charcoal))

            self.current_cah_sessions[GameKey]["members"].update({int(userid): {"cards": cards, "points": 0}})
            self.current_active_players.update({int(userid): GameKey})

        async def stop_cah_game(self, userid: int, fromtimeout:bool=False) -> str:
            """
            stops the game the userid is owner of and returns its key.
            """
            if userid not in self.current_active_players:
                raise self.errors.NotInAGame("You arent even in a game!")
            else:
                GameKey = self.current_active_players[userid]
            game = self.current_cah_sessions[GameKey]

            if game["owner"] != userid:
                raise self.errors.NotGameOwner("You need to be the game owner to start the game!")

            players = [Bot.get_user(playerid) for playerid in game["members"]]

            pointlist = [(self.current_cah_sessions[GameKey]["members"][player.id]["points"], player) for player in players]
            pointlist.sort(reverse=True, key=lambda x: x[0])
            for player in players:
                embed = discord.Embed(title=f"Game ended by {'lack of activity' if fromtimeout else 'owner'}, current leaderboard:", description="\n".join([f"{item[1].name} ({item[0]} point{'' if item[0] == 1 else 's'}){'  **(You)**' if player == item[1] else ''}" for item in pointlist]))
                await player.send(embed=embed)

            self.current_cah_sessions.pop(GameKey)

        async def leave_cah_game(self, userid) -> str: #make close the game when theres no players left
            if int(userid) not in self.current_active_players:
                raise self.errors.NotInAGame("You arent even in a game!")
            else:
                GameKey = self.current_active_players[userid]

                self.current_cah_sessions[GameKey]["members"].pop(userid)
                self.current_active_players.pop(userid)
                leftuser = Bot.get_user(userid)

                if userid == self.current_cah_sessions[GameKey]["owner"] and len(self.current_cah_sessions[GameKey]["members"]) > 1:
                    newowner = random.choice(list(self.current_cah_sessions[GameKey]["members"].keys()))
                    self.current_cah_sessions[GameKey]["owner"] = newowner


                for member in self.current_cah_sessions[GameKey]["members"]:
                    leftembed = discord.Embed(colour=general_utils.Colours.charcoal)
                    if newowner == member:
                        leftembed.title=f"{leftuser} just left, making you the new owner!"
                    else:
                        leftembed.title=f"{leftuser} just left!"

                    await Bot.get_user(member).send(embed=leftembed)

                if len(self.current_cah_sessions[GameKey]["members"]) == 0:
                    self.current_cah_sessions.pop(GameKey)

                return GameKey

        def combine_cards(self, black: str, whites: list) -> str:
            """
            Combines a black card with the given white cards.
            """
            result = black
            for white in whites:
                result = result.replace("_", f"` `__**{white}**__` `", 1)
            
            result = f"`{result}`"
            return result

        def get_cah_info(self, userid):
            if userid not in Bot.cah.current_active_players:
                raise self.errors.NotInAGame
            GameKey = Bot.cah.current_active_players[userid]
            game = self.current_cah_sessions[GameKey]
            players = [Bot.get_user(userid) for userid in game["members"]]
            info = {}
            info.update({"key": GameKey})
            info.update({"state": game['state']})

            pointlist = [(self.current_cah_sessions[GameKey]["members"][player.id]["points"], player) for player in players]
            pointlist.sort(reverse=True, key=lambda x: x[0])

            leaderboard = "\n".join([f" - {item[1].name}, {item[0]} point{'' if item[0] == 1 else 's'}{' **(Owner)**' if game['owner'] == item[1].id else ''}" for item in pointlist])

            info.update({"leaderboard": leaderboard})
            

        async def run_cah_game(self, owner_id):
            if owner_id not in self.current_active_players:
                raise self.errors.NotInAGame("You arent in a game yet!")
            GameKey = Bot.cah.current_active_players[owner_id]
            game = self.current_cah_sessions[GameKey]
            print(GameKey, game)
            if len(game["members"]) <= 1:
                raise self.errors.NotEnoughPlayers("You need more players to start")
            if game["owner"] != owner_id:
                raise self.errors.NotGameOwner("You need to be the game owner to start the game!")
            game["state"] = "in_progress"

            #await owner.send(f"starting game {GameKey}.")
            while GameKey in self.current_cah_sessions:#max([self.current_cah_sessions[GameKey]["members"][player.id]["points"] for player in players]) < 10:
                
                owner = Bot.get_user(owner_id)
                players = [Bot.get_user(userid) for userid in game["members"]]
                #print(players, owner)
                czar = random.choice(players)

                cur_black_card = database_utils.fetch_cards("black", 1)[0][1]
                if cur_black_card.count("_") == 0:
                    cur_black_card = cur_black_card+" _"
                #print(cur_black_card, czar)

                picked_cards = []
                #print(1)
                await asyncio.sleep(2)
                round_num = sum([self.current_cah_sessions[GameKey]["members"][player.id]["points"] for player in players])+1
                for player in players:
                    await player.send(embed=general_utils.format_embed(player, discord.Embed(title=f"Round {round_num} has started!"), "charcoal", False))
                pointlist = [(self.current_cah_sessions[GameKey]["members"][player.id]["points"], player) for player in players]
                pointlist.sort(reverse=True, key=lambda x: x[0])

                leaderboard = "\n".join([f" - {item[1].name}, {item[0]} point{'' if item[0] == 1 else 's'}{' **(Owner)**' if game['owner'] == item[1].id else ''}" for item in pointlist])

                #make it send leaderboard every 5 rounds

                await asyncio.sleep(5)
                #pointlist.sort(reverse=True, key=lambda x: x[0])
                ##print(3)
                #for player in players:
                #    embed = discord.Embed(title="Current leaderboard:", description="\n".join([f" - {item[1].name} ({item[0]} point{'' if item[0] == 1 else 's'}){'  **(You)**' if player == item[1] else ''}" for item in pointlist]))
                #    await player.send(embed=embed)
                #print(4)

                embed = discord.Embed(title="You are the card czar!", description=f"This is your black card:\n`{cur_black_card}`\n\nYour friends are currently choosing their white card(s), hang tight...", colour=general_utils.Colours.charcoal)
                await czar.send(embed=embed)
                #print(5)

                picked_embed = discord.Embed(title=f"People currently choosing:", description="\n".join([f"{':x:' if player.id not in [card[1] for card in picked_cards] else ':white_check_mark:'} | {player.name}" for player in players if player != czar]))
                picked_embed.set_footer(text=f"{(len(players)-1)-len(picked_cards)} player{'' if (len(players)-1)-len(picked_cards) == 1 else 's'} remaining...")
                picked_embed_message = await czar.send(embed=picked_embed)

                #print(6)
                msgs = {}
                for player in players:
                    if player != czar:
                        embed = discord.Embed(title=f"{czar} is the card czar!", description=f"`{cur_black_card}`")
                        await player.send(embed=embed)
                        cards = '\n'.join([f"**[ {index} ]** `{card}`" for index, card in enumerate(game['members'][player.id]['cards'])]) # has started, you have these cards:\n`{cards}`"
                        embed = discord.Embed(colour=general_utils.Colours.silver, title=f"These are your cards, chooose __**{cur_black_card.count('_')}**__ and send their respective numbers, separated by commas.", description=cards) #__**{cur_black_card.count('_')}**__
                        msg = await player.send(embed=embed)
                        msgs.update({player.id: msg})
                        #card_preview = await player.send(embed=discord.Embed(title="Card preview:", colour=general_utils.Colours.charcoal, description=f"`{}`"))

                #print(7)
                while len(picked_cards) < len(players)-1:

                    check = lambda m: m.channel.id in [player.dm_channel.id for player in players if player.id not in [e[1] for e in picked_cards]] and general_utils.represents_int(m.content) == True and int(m.content) <= len(game['members'][m.author.id]['cards'])
                    try:
                        msg = await Bot.wait_for('message', timeout=3600.0, check=check)
                    except asyncio.TimeoutError:
                        for player in players:
                            await player.send(embed=discord.Embed(title="People took too long to respond... (1h timeout, game ended)", colour=general_utils.Colours.red))
                        
                        await self.stop_cah_game(owner.id, True)
                        return
                    #parse response
                    response = msg.content
                    response = [int(x) for x in response.replace(" ", "").split(", ")]
                    if len(response) != cur_black_card.count("_"):
                        await msg.author.send(f"You gave the incorrect number of cards! ({len(response)} out of the {cur_black_card.count('_')} needed)")
                        continue
                    did_error = False
                    for index, number in enumerate(response):

                        if number > len(self.current_cah_sessions[GameKey]["members"][msg.author.id]["cards"]):
                            await msg.author.send("One of the numbers you gave didnt have a corresponding card! please try again.")
                            did_error = True
                            break
                        if did_error:
                            break

                        response[index] = self.current_cah_sessions[GameKey]["members"][msg.author.id]["cards"][number]

                        print(cur_black_card, response)
                        await msgs[msg.author.id].edit(embed=general_utils.format_embed(msg.author, discord.Embed(title="This is your chosen combo:", description=self.combine_cards(black=cur_black_card, whites=response)), "charcoal", False, False))

                    print(response)
                    picked_card = [response, msg.author]
                    #embed = discord.Embed(title=f"({len(picked_cards)}/{len(players)-1})")
                    #embed.set_author(icon_url=msg.author.avatar_url, name=f"{msg.author} has chosen their card!")
                    #await czar.send(embed=embed)
                    #await owner.send(f"{msg.author}: {picked_card[0]}")

                    picked_cards += [picked_card]

                    picked_embed = discord.Embed(title=f"Currently chosen:", description="\n".join([f"{':x:' if player.id not in [card[1].id for card in picked_cards] else ':white_check_mark:'} | {player.name}" for player in players if player != czar]))
                    picked_embed.set_footer(text=f"{(len(players)-1)-len(picked_cards)} players remaining...")
                    await picked_embed_message.edit(embed=picked_embed)

                embed = discord.Embed(title="Everyone has picked, here are their cards:", description="\n".join([(f"**[ {index} ]** `"+("`, `".join(card[0]))) for index, card in enumerate(picked_cards)])+'`', colour=general_utils.Colours.silver)
                await picked_embed_message.edit(embed=embed)
                embed = discord.Embed(title="Send the number of the funniest card combination!")#, description=f"The black card is:\n`{cur_black_card}`")
                await czar.send(embed=embed)

                check = lambda m: m.channel.id == czar.dm_channel.id and general_utils.represents_int(m.content) == True and int(m.content) <= len(picked_cards)

                try:
                    msg = await Bot.wait_for('message', timeout=3600.0, check=check)
                except asyncio.TimeoutError:
                    for player in players:
                        await player.send(embed=discord.Embed(title="Czar took too long to respond... (1h timeout, game ended)", colour=general_utils.Colours.red))
                    await self.stop_cah_game(owner.id, True)
                    return


                winning_card = picked_cards[int(msg.content)]
                print(cur_black_card, winning_card[0])
                winning_combo = self.combine_cards(black=cur_black_card, whites=winning_card[0]) 

                self.current_cah_sessions[GameKey]["members"][winning_card[1].id]["points"] += 1
                embed = discord.Embed(colour=general_utils.Colours.silver, title=f"You have picked {winning_card[1].name}'s combination!", description=winning_combo)
                await czar.send(embed=embed)

                for player in players:
                    if player.id == czar.id:
                        continue
                    elif player.id == winning_card[1].id:
                        embed = discord.Embed(colour=general_utils.Colours.silver, title=f"Your combination was picked by the czar! (+1 point)", description=winning_combo)
                        await player.send(embed=embed)
                    else:
                        embed = discord.Embed(colour=general_utils.Colours.silver, title=f"{winning_card[1].name}'s combination was picked by the czar!", description=winning_combo)
                        await player.send(embed=embed)
            
            max_score = 0
            for player in players:
                max_score = max([self.current_cah_sessions[GameKey]["members"][player.id]["points"], max_score])
            winners = []
            for player in players:
                if self.current_cah_sessions[GameKey]["members"][player.id]["points"] == max_score:
                    winners += [player]

            for player in players:
                if player not in winners:
                    await player.send(embed=discord.Embed(title=f"{', '.join([winner.name for winner in winners[1:]])}{f'and {winners[1]}' if len(winners) > 1 else ''} won with {max_score} points!"))
                else:
                    winners.pop(player)
                    await player.send(embed=discord.Embed(title=f"{', '.join(['You']+[winner.name for winner in winners[1:]]) if len(winners) > 0 else ''}{f'and {winners[1]}' if len(winners) > 1 else ''} won with {max_score} points!"))
                    winners += [player]
    Bot.cah = cah()