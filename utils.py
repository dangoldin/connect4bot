import copy

class utils:

    def isValidMove(self, board, column):
        try:
            board[column].index(0)
            return True
        except:
            return False
    
    def copyBoard(self, board):
        return 

    def getRowOfMove(self, board, column):
        reversed_col = board[column][::-1]
        return len(reversed_col) - 1 - reversed_col.index(0)

    def move(self, board, player, column):
        next_move = self.getRowOfMove(board, column)
        board[column][next_move] = player
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
        for i in range(desired):
            #print 'P %d (%d, %d)' % (player, ic, ir)
            try:
                if ir >= 0 and ic >= 0 and board[ic][ir] == player:
                    cnt += 1
            except:
                return 0
            if 'U' in dir:
                ir -= 1
            if 'D' in dir:
                ir += 1
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
                print board[j][i],
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
        # Outer layer 
        # Edge pieces same
        #eps = self.getEdgePieces(board, player, True)
        # Edge pieces other
        #epo = self.getEdgePieces(board, player, False)
        # Num 3 lines
        nlts = self.getNumLines(board, player, column, 3, True)
        nlto = self.getNumLines(board, player, column, 3, False)
        # Num rows
        nr = self.getNumRows(board, column)
        # Same in col
        # Other in col
        return (9, aps, apo, nlts, nlto, nr)
    
    def getAdjacentPieces(self, board, player, column, same_player):
        pieces = 0
        row = self.getRowOfMove(board, column)
        for x in (-1,0,1):
            for y in (-1,0,1):
                r_idx = row + x
                c_idx = column + y
                if r_idx >= 0 and c_idx >= 0:
                    try:
                        if same_player:
                            if board[c_idx][r_idx] == player:
                                pieces += 1
                        else:
                            if board[c_idx][r_idx] <> player and board[c_idx][r_idx] > 0:
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
        cols, rows = self.getBoardDims(board)
        dirs = ['U', 'R', 'UR', 'UL']

        if not same_player:
            new_player = (player % 2) + 1
        else:
            new_player = player

        board = copy.deepcopy(board)
        board = self.move(board, new_player, column)

        num_lines = 0
        for i in range(rows):
            for j in range(cols):
                if board[j][i] <> 0:
                    for dir in dirs:
                        whose_line = self.isLine(board, j, i, dir, desired=length)
                        if whose_line <> 0:
                            #print new_player,j,i,dir
                            num_lines += 1
        return num_lines
    
    def getNumRows(self, board, column):
        return len(board[column]) - board[column].count(0)
