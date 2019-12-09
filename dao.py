from authentication import User


class DAO:
    """
    An abstraction of a data store for more testable code.

    Args:
        connection: a sqlite3 database connection

    """

    def __init__(self, connection):
        self.connection = connection

    def getUserByUsername(self, username):
        """
        Get a User object from the datastore.

        Args:
            username: the username of the desired user

        """
        c = self.connection.cursor()

        c.execute("select uid, password from users where username=?;",
                  (username,))

        row = c.fetchone()

        if row is None:
            return None

        return User(self, row[0], username, row[1])

    def getUserByUid(self, uid):
        """
        Get a User object from the datastore.

        Args:
            uid: the user id of the desired user

        """
        c = self.connection.cursor()

        c.execute("select username, password from users where uid=?;",
                  (uid,))

        row = c.fetchone()

        if row is None:
            return None

        return User(self, uid, row[0], row[1])

    def registerNewUser(self, username, shadowEntry):
        """
        Go to the datastore and create a new entry for a user.

        Args:
            username: string username of the new user
            shadowEntry: ShadowEntry instance of hashed password

        """
        c = self.connection.cursor()

        c.execute("insert into users(username, password) values(?, ?)",
                  (username, shadowEntry.__str__()))

        self.connection.commit()

    def saveGame(self, winnerID, loserID, time=None):
        """
        Go to the datastore and create a new entry for a game.

        Args:
            winnerID: int id of the game's winner
            loserID: int id of the game's loser
            time: datetime instance when the game was won

        """
        c = self.connection.cursor()

        c.execute("insert into games(winner_id, loser_id, time) values(?, ?, ?)",
                  (winnerID, loserID, time))

        self.connection.commit()

    def getGame(self, gameID):
        """
        Go to the datastore and fetch the entry for given id.

        Args:
            gameID: int id of the desired game

        """
        c = self.connection.cursor()

        c.execute("select winner_id, loser_id, time from games where game_id=?",
                  (gameID,))

        return c.fetchone()

    def getScore(self, uid):
        """
        Go to the datastore and calculate won - loss games.

        Args:
            uid: int id of desired user

        """
        c = self.connection.cursor()

        # there is almost certainly a better way to do this
        c.execute("select count(*) from games where winner_id=?",
                  (uid,))
        won = c.fetchone()[0]

        c.execute("select count(*) from games where loser_id=?",
                  (uid,))
        lost = c.fetchone()[0]

        return won - lost
