from Game import Game, fetchCoordinate
from Player import getPlayerByPiece, getPlayers

import datetime

pieces = ['x', 'o']
players = getPlayers(pieces)

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

print(f'{getPlayerByPiece(game.winner, players).name} wins')

now = datetime.datetime.now()
print(now)
