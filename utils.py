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

    def isLine(self, board, col, row, dir, desired = 4):
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
        if cnt == desired:
            #print 'Found winner %d (%d, %d, %s)' % (player, col, row, dir)
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
    
    def getFreeCols(self, board):
        return [i for i,col in enumerate(board) if col.count(0) > 0]
    
    def getStats(self, board, player, column):
        # Adjacent pieces same
        aps = self.getAdjacentPieces(board, player, column, True)
        # Adjacent pieces other
        apo = self.getAdjacentPieces(board, player, column, False)
        # Edge pieces same
        eps = self.getEdgePieces(board, player, True)
        # Edge pieces other
        epo = self.getEdgePieces(board, player, False)
        # Num 3 lines
        nlt = self.getNumLines(board, player, column, 3, True)
        # Same in col
        # Other in col
        return (aps, apo, eps, epo, nlt)
        #return {
        #    'aps': aps,
        #    'apo': apo,
        #    'eps': eps,
        #    'epo': epo,
        #}
    
    def getAdjacentPieces(self, board, player, column, same_player):
        pieces = 0
        row = board[column].index(0)
        for x in (-1,0,1):
            for y in (-1,0,1):
                try:
                    if same_player:
                        if board[column + y][row + x] == player:
                            pieces += 1
                    else:
                        if board[column + y][row + x] <> player and board[column + y][row + x] > 0:
                            pieces += 1
                except:
                    pass
        return pieces
    
    def getEdgePieces(self, board, player, same_player):
        pieces = 0
        if same_player:
            # cols
            pieces += board[0].count(player)
            pieces += board[-1].count(player)
            # rows
            pieces += sum([1 for col in board if col[0] == player])
            pieces += sum([1 for col in board if col[-1] == player])
        else:
            # cols
            pieces += len(board[0]) - board[0].count(player) - board[0].count(0)
            pieces += len(board[-1]) - board[-1].count(player) - board[-1].count(0)
            # rows
            pieces += sum([1 for col in board if col[0] <> player and col[0] > 0])
            pieces += sum([1 for col in board if col[-1] <> player and col[0] > 0])
        return pieces
    
    def getNumLines(self, board, player, column, length, same_player):
        dirs = ['U', 'R', 'UR', 'UL']
        row = board[column].index(0)
        board[column][row] = player
        num_lines = 0
        for d in dirs:
            if same_player:
                if self.isLine(board, column, row, d, length):
                    num_lines += 1
        board[column][row] = 0
        return num_lines