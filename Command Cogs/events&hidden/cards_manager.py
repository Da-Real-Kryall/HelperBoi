import random, discord
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

                cards = database_utils.fetch_cards("white", 7)

                self.current_active_players.update({owner_id: GameKey})
                self.current_cah_sessions.update({
                    GameKey: {
                        "owner": owner_id,
                        "state": "starting",
                        "members": {
                            owner_id: {
                                "cards": cards,
                                "points": 0
                            }
                        }
                    }
                })
            return GameKey
        
        async def join_cah_game(self, userid, GameKey):
            if userid in self.current_active_players:
                raise self.errors.AlreadyInGame("Player is already part of another game!")
            cards = database_utils.fetch_cards("white", 7)

            joineduser = Bot.get_user(userid)
            for member in self.current_cah_sessions[GameKey]["members"]:
                await Bot.get_user(member).send(embed=discord.Embed(title=f"{joineduser} just joined!", colour=general_utils.Colours.charcoal))

            self.current_cah_sessions[GameKey]["members"].update({userid: {"cards": cards, "points": 0}})

        async def leave_cah_game(self, userid) -> str:
            if userid not in self.current_active_players:
                raise self.errors.NotInAGame("You arent even in a game!")
            else:
                GameKey = self.current_active_players[userid]

                self.current_cah_sessions[GameKey]["members"].pop(userid)
                leftuser = Bot.get_user(userid)

                if userid == self.current_cah_sessions[GameKey]["owner"]:
                    newowner = random.choice(list(self.current_cah_sessions[GameKey]["members"].keys()))
                    self.current_cah_sessions[GameKey]["owner"] = newowner


                for member in self.current_cah_sessions[GameKey]["members"]:
                    leftembed = discord.Embed(colour=general_utils.Colours.charcoal)
                    if newowner == member:
                        leftembed.title=f"{leftuser} just left, making you the new owner!"
                    else:
                        leftembed.title=f"{leftuser} just left!"

                    await Bot.get_user(member).send(embed=leftembed)

                return GameKey

        async def run_cah_game(self, owner_id):
            if owner_id not in self.current_cah_sessions:
                raise self.errors.NotInAGame("You arent in a game yet!")
            GameKey = Bot.cah.current_active_players[owner_id]
            game = self.current_cah_sessions[GameKey]
            if game["owner"] != owner_id:
                raise self.errors.NotGameOwner("You need to be the game owner to start the game!")
            owner = Bot.get_user(owner_id)
            game["state"] = "in_progress"
            players = [Bot.get_user(userid) for userid in game["members"]]

            #await owner.send(f"starting game {GameKey}.")

            for player in players:
                cards = '`\n`'.join([card[1] for card in game['members'][player.id]['cards']]) # has started, you have these cards:\n`{cards}`"
                await player.send(embed=discord.Embed(colour=general_utils.Colours.charcoal, title=f"Game is starting..."))
            
            card_czar = random.choice(players)

            await card_czar.send(f"You are the czar!")

            for player in players:
                if player != card_czar:
                    await player.send(f"{card_czar} is the card czar.")
            
    
    Bot.cah = cah()