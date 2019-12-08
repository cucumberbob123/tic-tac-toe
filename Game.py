from Player import Player


class Game:
    def __init__(self, x, y, players):
        self.x = x
        self.y = y

        if len(players) != 2:
            raise ValueError("players must be a list of length 2")
        if not all(type(player) == Player for player in players):
            raise ValueError("players must be a list of Players")

        self.players = players

        # this way is less nice that multiplying strings, but it works
        self.board = []
        for _ in range(y):
            self.board.append(['-'] * x)

    def __str__(self):
        stringified = ''
        for i in self.board:
            for j in i:
                stringified += j
            stringified += '\n'
        return stringified[:-1]

    def place(self, x, y, team):
        if team not in ['x', 'o']:
            raise TypeError('Invalid player')

        # if it's already been placed...
        if self.board[self.y - 1 - y][x] != '-':
            return False

        self.board[self.y - 1 - y][x] = team
        return True

    def won(self):
        # check verticals
        for i in range(len(self.board)):
            if self.board[i][0] == '-':
                continue
            if all(x == self.board[i][0] for x in self.board[i]):
                self.winner = self.board[i][0]
                return True

        # check horizontals
        for i in range(self.y):
            if self.board[0][i] == '-':
                continue
            if all(self.board[x][i] == self.board[0][i] for x in range(self.x)):
                self.winner = self.board[0][i]
                return True

        # check diagonals, iff it's a square board
        if self.x == self.y:
            # checks -ve diags
            if self.board[self.y - 1][self.x - 1] != '-':
                if all(self.board[self.y - 1 - i][i] == self.board[self.y - 1][self.x - 1] for i in range(self.x)):
                    self.winner = self.board[self.y - 1][self.x - 1]
                    return True

            # checks +ve diags
            if self.board[self.y - 1][0] != '-':
                if all(self.board[i][self.x - 1 - i] == self.board[self.y - 1][0] for i in range(self.x)):
                    self.winner = self.board[self.y - 1][0]
                    return True

        return False


def fetchCoordinate(axis):
    coordinate = input(f'{axis}-coordinate: ')

    if coordinate == '':
        print('please enter something')
        fetchCoordinate(axis)

    if coordinate not in '1234567890':
        print('please guess a number')
        fetchCoordinate(axis)

    return int(coordinate)
