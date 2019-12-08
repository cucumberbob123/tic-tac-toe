from authentication import login, register, getPassword, getUsername


class Player:
    """
    A player of a game.

    Args:
        piece: the game piece the player is using
        creds: user's credentials to log in

    Attributes:
        score: the user's score so far

    """

    def __init__(self, piece, creds=None):
        if creds is not None:
            if not self.validCredentials(creds):
                raise ValueError("Credentials are invalid")
            else:
                self.creds = creds

        self.score = 0
        self.piece = piece

        try:
            self.name = creds["username"]
        except TypeError:
            self.name = piece

    def incScore(self):
        self.score += 1

    def validCredentials(self, credentials):
        return True


def getPlayerByPiece(piece, players):
    """
    Find a player from a list of players by piece.

    Args:
        piece: the game piece the desired player uses.
        players: a list of players of type Player

    Returns:
        Player: the desired player

    """
    for player in players:
        if player.piece == piece:
            return player
    return None


def getPlayers(pieces):
    """
    Go to stdout to get len(pieces) to login, register or remain anonymous.

    Args:
        pieces: a list of string game pieces

    """
    players = []
    for i in range(len(pieces)):
        print(f"Player {i+1}")
        if input("Type skip to skip login: ") == "skip":
            players.append(Player(pieces[i]))
            print("\n\n")
            continue

        userHasAccount = ""
        while userHasAccount not in ['y', 'n']:
            userHasAccount = input("Do you have an account [y/n]: ")

        if userHasAccount == 'y':
            username = password = ""
            while not login(username, password, ""):
                username = getUsername()
                password = getPassword()

            print("Successfully logged in")

        else:
            username = password = ""
            while not register(username, password, ""):
                username = getUsername()
                password = getPassword()
            print("Account successfully created!")

        creds = {"username": username, "password": password}
        players.append(Player(pieces[i], creds))

        print("\n\n")

    return players
