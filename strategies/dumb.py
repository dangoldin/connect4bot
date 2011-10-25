import random
from strategy import strategy

class dumb(strategy):
    
    def getMove(self, board_json):
        board = self.getBoard(board_json)
        cols, rows = self.utils.getBoardDims(board)
        
        valid_cols = [i for i, col in enumerate(board) if col.count(0) > 0]
        #print valid_cols
        column = random.choice(valid_cols)
        return column