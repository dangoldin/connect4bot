import random

class c4:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = self.initBoard()
       
    def initBoard(self):
        board = []
        for i in range(self.cols):
            board.append( [0] * self.rows )
        return board
        #return [[0] * self.rows] * self.cols
    def isValidMove(self, player, column):
        try:
            self.board[column].index(0)
            return True
        except:
            return False
       
    def move(self, player, column):
        self.board[column][ self.board[column].index(0) ] = player
    def isWinner(self):
        # Don't really need to check all 8 dirs since they are symmetrical
        #dirs = ['U', 'D', 'L', 'R', 'UL', 'UR', 'DL', 'DR']
        dirs = ['U', 'R', 'UR', 'UL']
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[j][i] <> 0:
                    for dir in dirs:
                        winner = self.isLine(j, i, dir)
                        if winner <> 0:
                            return winner
        return 0
       
    def isLine(self, col, row, dir):
        player = self.board[col][row]
        cnt = 0
        ic, ir = col, row
        #print "Player %d" % player
        for i in range(4):
            #print '(%d, %d)' % (ic, ir)
            try:
                if ir >= 0 and ic >= 0 and self.board[ic][ir] == player:
                    cnt += 1
            except:
                return 0
            if 'U' in dir:
                ir += 1
            if 'D' in dir:
                ir -= 1
            if 'R' in dir:
                ic += 1
            if 'L' in dir:
                ic -= 1
        if cnt == 4:
            print 'Found winner %d (%d, %d, %s)' % (player, col, row, dir)
            return player
        return 0
    def printBoard(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print self.board[j][self.rows - i - 1],
            print "\n",
        print "\n",
       
if __name__ == "__main__":
    c = c4()
    c.printBoard()
    for i in range(42):
        winner = c.isWinner()
        if winner <> 0:
            print 'Player %d has won' % winner
            exit()
        player = (i % 2) + 1
        invalidMove = True
        while invalidMove:
            column = random.randint(0,c.cols - 1)
            invalidMove = not c.isValidMove(player, column)
        c.move(player, column)
        c.printBoard()
