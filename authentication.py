import string
import random
import hashlib


def getUsername():
    username = ""
    while not username.isalpha():
        username = input("Username: ")
    return username


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
    Abstraction to handle loggin in/ registration.

    NOTE the authenticator stores the salt/hash combination as a
         shadow entry. This is the same format as etc/shadow in a linux
         system. the format is ${hash_type}${salt}${password}

    """

    def __init__(self, dao):
        self.dao = dao

    def userExists(self, username):
        user = self.dao.getUserByUsername(username)
        return user is not None

    def register(self, username, password):
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

        return self.getShadowEntry(username).validate(password)

    def getShadowEntry(self, username):
        user = self.dao.getUserByUsername(username)
        return ShadowEntry.fromString(user.password)


class UsernameError(Exception):
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
    def __init__(self, uid, username, password):
        self.uid = uid
        self.username = username
        self.password = password


class Attempt:
    def __init__(self, dao, uid, score, time):
        self.dao = dao
        self.score = score
        self.time = time

        self.user = dao.getUserByUid(uid)
