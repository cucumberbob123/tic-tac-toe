import datetime
from Game import Game
from Player import getPlayers

from dao import DAO
import sqlite3

connection = sqlite3.connect("scores.db")
dao = DAO(connection)


pieces = ['x', 'o']
players = getPlayers(pieces, dao)

game = Game(3, 3, players)

print(game)

game.place(0, 0, 'x')
game.place(1, 1, 'x')
game.place(2, 2, 'x')

print(game)

game.won()

print(f'{game.winner.id} wins')

print(f"{game.loser.id} loses")

now = datetime.datetime.now()

if not (game.loser.id == 0 and game.winner.id == 0):
    print('got here')
    dao.saveGame(game.winner.id, game.loser.id)
