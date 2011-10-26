import random, json
from strategies import dumb, genetic
import utils
from collections import defaultdict

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
    #players = [ dumb.dumb(1), dumb.dumb(2) ]
    #players = [ dumb.url(1,'http://dl.no.de/ai/twostep/move'), genetic.genetic(2, 'best.c4') ]
    #players = [ dumb.url(1,'http://dl.no.de/ai/random/move'), genetic.genetic(2, 'best.c4') ]
    #players = [ genetic.genetic(1, 'best.c4'), dumb.url(2,'http://dl.no.de/ai/random/move') ]
    #players = [ genetic.genetic(1, 'best_so_far2.c4'), dumb.dumb(2) ]
    #players = [ genetic.genetic(1, 'best_so_far2.c4'), dumb.url(2,'http://dl.no.de/ai/twostep/move') ]
    #players = [ genetic.genetic(1, 'best.c4'), dumb.url(2,'http://dl.no.de/ai/twostep/move') ]
    players = [ genetic.genetic(1, 'best.c4'), dumb.dumb(1) ]
    NUM_GAMES = 200 
    ROWS = 6
    COLS = 7

    win_stats = defaultdict(int)
    for g in range(NUM_GAMES):
        c = c4(rows=ROWS,cols=COLS)
        for i in range(c.rows * c.cols):
            #c.printBoard()
            winner = c.isWinner()
            if winner <> 0:
                print 'Player %d has won' % winner
                #c.printBoard()
                #exit()
                break
            player = (i % 2)
            board = c.getBoard(is_json=False)
            json_state = json.dumps( { "rows":ROWS,
                                       "cols":COLS,
                                       "board":board,
                                       "currentTurn":player+1,
                                       "moveNumber":i} )
            column = players[player].getMoveJSON(json_state)
            #print player, column
            #if player == 1:
            #    print 'Stats: ', column, c.utils.getStats(board, player+1, column)
            c.move(players[player].getPlayer(), column)
        win_stats[winner] += 1
    print 'Win Stats: 1: %d, 2: %d, 0 %d - 1: %f, 2: %f' % \
        (win_stats[1], win_stats[2], win_stats[0], (0.5*win_stats[0] + 1.0*win_stats[1])/NUM_GAMES, (0.5*win_stats[0]+1.0*win_stats[2])/NUM_GAMES)