import string
import random
import hashlib


def getUsername():
    """TODO ensure username is in dao before returning"""
    return input("Username")


def getPassword():
    return input("Password: ")


def login(username, password, dao):
    if username == "" or password == "":
        return False
    return True


def register(username, password, dao):
    if username == "" or password == "":
        return False
    return True


class Authenticator:
    """
    Abstraction to handle loggin in/registration.

    The authenticator stores the salt/hash combination as an instance of
    ShadowEntry. This is an abstraction on top of the same format
    as etc/shadow in a linux system. the format is:
        ${hash_type}${salt}${password}

    """

    def __init__(self, dao):
        self.dao = dao

    def userExists(self, username):
        user = self.dao.getUserByUsername(username)
        return user is not None

    def register(self, username, password):
        """Register a new user."""
        if username == "" or password == "":
            return

        if self.userExists(username):
            raise UsernameError("username taken")

        shadowEntry = ShadowEntry.generate(password)

        self.dao.registerNewUser(username, shadowEntry)

        return True

    def login(self, username, password):
        if username == "" or password == "":
            return

        if not self.userExists(username):
            raise UsernameError("Username not found")

        if not self.getShadowEntry(username).validate(password):
            raise PasswordError("Incorrect password")

    def getShadowEntry(self, username):
        user = self.dao.getUserByUsername(username)
        return ShadowEntry.fromString(user.password)


class UsernameError(Exception):
    pass


class PasswordError(Exception):
    pass


class ShadowEntry:
    def __init__(self, type_, salt, hashedPassword):
        self.salt = salt
        self.type = type_
        self.hashedPassword = hashedPassword

    def __str__(self):
        """doctring"""
        return f"${self.type}${self.salt}${self.hashedPassword}"

    def validate(self, password):
        if self.type != 5:
            return False
        expected = self._generate_hash(self.salt, password)

        return self.hashedPassword == expected

    @classmethod
    def generate(cls, password):
        salt = cls._generate_salt()
        hashedPassword = cls._generate_hash(salt, password)

        return ShadowEntry(5, salt, hashedPassword)

    @classmethod
    def fromString(cls, shadowString):
        salt, hashed_password = shadowString.split('$')[2:]
        return ShadowEntry(5, salt, hashed_password)

    @staticmethod
    def _generate_salt(length=4):
        chars = string.ascii_letters + string.digits

        salt = ""
        for i in range(length):
            salt += chars[random.randint(0, len(chars) - 1)]

        return salt

    @staticmethod
    def _generate_hash(salt, password):
        encoded = (salt + password).encode("utf-8")

        hasher = hashlib.sha256()
        hasher.update(encoded)

        return hasher.hexdigest()


class User:
    # TODO make this good
    def __init__(self, dao, uid, username, password):
        self.dao = dao

        self.uid = uid
        self.username = username
        self.password = password

    @classmethod
    def getUserFromInput(cls, dao, out, in_):
        # Improve me
        """
        Go to given out/input and get user to regiter or log in.

        Args:
            dao: dao instance to get login info from
            out: function to call to output text
            in_: function to call to get input from user
                 (note _ to avoid naming conflict)
        Returns:
            User: logged in instance of User

        """
        if in_("Type skip to skip login: ") == "skip":
            # uid=0 refers to anonymous user in db, useful for scoring etc.
            return User(dao, 0, None, None)

        userHasAccount = ""
        while userHasAccount not in ['y', 'n']:
            userHasAccount = in_("Do you have an account [y/n]: ")

        authn = Authenticator(dao)

        if userHasAccount == 'y':
            username = getUsername()
            password = getPassword()
            while True:
                try:
                    authn.login(username, password)
                    break

                except UsernameError:
                    out("Wrong username/password combo")
                    username = getUsername()
                    password = getPassword()

                except PasswordError:
                    out("Wrong password")
                    password = getPassword()

            out("Logged in!")
            return dao.getUserByUsername(username)

        else:
            username = getUsername()
            password = getPassword()
            while not authn.register(username, password):
                out("That username is already taken")
                username = getUsername()
                password = getPassword()

            out("Registered!")
            return dao.getUserByUsername(username)


class Attempt:
    def __init__(self, dao, uid, score, time):
        self.dao = dao
        self.score = score
        self.time = time

        self.user = dao.getUserByUid(uid)
