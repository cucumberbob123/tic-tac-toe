import datetime
from Game import Game, fetchCoordinate
from Player import getPlayers

from dao import DAO
import sqlite3

connection = sqlite3.connect("scores.db")
dao = DAO(connection)


pieces = ['x', 'o']
players = getPlayers(pieces, dao)

game = Game(3, 3, players)

turn = 0

print(game)

while not game.won():
    p = players[turn % 2]

    turn += 1

    print(f'{p.name}\'s turn')

    # get coordinates and ensure they are valid, and placed
    while True:
        x, y = fetchCoordinate('x'), fetchCoordinate('y')

        if game.place(x - 1, y - 1, p.piece):
            break
        else:
            print("looks like there's already a piece there, try elsewhere")
    print(game)

print(f'{game.winner.name} wins')

print(f"{game.loser.name} loses")

now = datetime.datetime.now()

if not all(player.id == 0 for player in players):
    dao.saveGame(game.winner.id, game.loser.id)
