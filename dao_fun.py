from authentication import Authenticator, ShadowEntry
from dao import DAO
import sqlite3
import datetime

connection = sqlite3.connect("scores.db")

# c = connection.cursor()

# c.execute("insert into scores(uid, score, time) values(1, 3, ?)", (None,))

# connection.commit()

dao = DAO(connection)

print(dao.getScore(1)[0].__dict__)
