import random, pickle
from operator import itemgetter, attrgetter

from strategy import strategy
from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts

def gp_add(a, b):
    return a + b
def gp_sub(a, b):
    return a - b
def gp_mul(a, b):
    return a * b
def gp_div(a, b):
    if b == 0:
        return a
    else:
        return a/b
def gp_igt(a, b, c, d):
    if a > b:
        return c
    else:
        return d

class genetic(strategy):

    def __init__(self, player, strat_file):
        strategy.__init__(self,player)
        self.strat_file = strat_file
        self.strat = compile(pickle.load(open(self.strat_file, 'rb')), "<string>", "eval")
    
    def getMove(self, board_json):
        board = self.getBoard(board_json)
        
        col_scores = []
        for col in self.utils.getFreeCols(board):
            aps, apo, eps, epo, nlt = self.utils.getStats(board,self.player,col)
            score = eval(self.strat)
            col_scores.append((score, col))
        random.shuffle(col_scores)
        sc = sorted(col_scores, key=itemgetter(0), reverse=True)
        #print 'Col Scores', str(sc)
        column = sc[0][1]
        return column