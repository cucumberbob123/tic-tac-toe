from authentication import User


class Player:
    """
    A player of a game.

    Args:
        piece: the game piece the player is using
        creds: user's credentials to log in

    Attributes:
        id: the player's id
        piece: the player's game piece
        name: username (if present) or their game piece

    """

    def __init__(self, piece, user=None):
        self.id = user.uid

        self.piece = piece

        if user.username is not None:
            self.name = user.username
        else:
            self.name = piece

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


def getPlayers(pieces, dao):
    """
    Go to stdout to get len(pieces) to login, register or remain anonymous.

    Args:
        pieces: a list of string game pieces

    """

    print("Welcome to tic - tac - toe!\n\n")

    players = []
    for i in range(len(pieces)):
        print(f"Player {i + 1}")
        user = User.getUserFromInput(dao, print, input)
        players.append(Player(pieces[i], user))

        print("\n\n")

    return players
