class utils:

    def isValidMove(self, board, column):
        try:
            board[column].index(0)
            return True
        except:
            return False
    
    def move(self, board, player, column):
        board[column][ board[column].index(0) ] = player
        return board
    
    def isWinner(self, board):
        cols, rows = self.getBoardDims(board)
        # Don't really need to check all 8 dirs since they are symmetrical
        #dirs = ['U', 'D', 'L', 'R', 'UL', 'UR', 'DL', 'DR']
        dirs = ['U', 'R', 'UR', 'UL']
        for i in range(rows):
            for j in range(cols):
                if board[j][i] <> 0:
                    for dir in dirs:
                        winner = self.isLine(board, j, i, dir)
                        if winner <> 0:
                            return winner
        return 0

    def isLine(self, board, col, row, dir):
        player = board[col][row]
        cnt = 0
        ic, ir = col, row
        #print "Player %d" % player
        for i in range(4):
            #print '(%d, %d)' % (ic, ir)
            try:
                if ir >= 0 and ic >= 0 and board[ic][ir] == player:
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

    def printBoard(self, board):
        cols, rows = self.getBoardDims(board)
        for i in range(rows):
            for j in range(cols):
                print board[j][rows - i - 1],
            print "\n",
        print "\n",
    
    def getBoardDims(self, board):
        cols = len(board)
        rows = len(board[0])
        return (cols, rows)