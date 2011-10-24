import random
from strategy import strategy

class smarter(strategy):
    
    def getMove(self, board_json):
        board = self.getBoard(board_json)
        cols, rows = self.utils.getBoardDims(board)
        
        invalidMove = True
        while invalidMove:
            column = random.randint(0,cols - 1)
            invalidMove = not self.utils.isValidMove(board, column)
        return column