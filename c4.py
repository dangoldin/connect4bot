import random, json
from strategies import dumb
import utils

class c4:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = self.initBoard()
        self.utils = utils.utils()
    
    def getBoard(self, is_json=False):
        if is_json:
            return json.dumps(self.board)
        else:
            return self.board
       
    def initBoard(self):
        board = []
        for i in range(self.cols):
            board.append( [0] * self.rows )
        return board
        #return [[0] * self.rows] * self.cols

    def isValidMove(self, column):
        return self.utils.isValidMove(self.board, column)
       
    def move(self, player, column):
        self.board = self.utils.move(self.board, player, column)
    
    def isWinner(self):
        return self.utils.isWinner(self.board)
    
    def printBoard(self):
        self.utils.printBoard(self.board)
       
if __name__ == "__main__":
    players = [ dumb.dumb(1), dumb.dumb(2) ]
    
    c = c4(rows=6,cols=7)
    for i in range(c.rows * c.cols):
        c.printBoard()
        winner = c.isWinner()
        if winner <> 0:
            print 'Player %d has won' % winner
            exit()
        player = (i % 2)
        board_json = c.getBoard(is_json=True)
        column = players[player].getMove(board_json)
        c.move(players[player].getPlayer(), column)
