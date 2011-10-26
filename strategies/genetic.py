import random, pickle
from operator import itemgetter, attrgetter

from strategy import strategy
from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts

from gp_funcs import gp_add, gp_sub, gp_mul, gp_igt

class genetic(strategy):

    def __init__(self, player, strat_file):
        strategy.__init__(self,player)
        self.strat_file = strat_file
        self.strat = compile(pickle.load(open(self.strat_file, 'rb')), "<string>", "eval")
    
    def getMove(self, board):
        col_scores = []
        for col in self.utils.getFreeCols(board):
            const, aps, apo, nlts, nlto, nr = self.utils.getStats(board,self.player,col)
            score = eval(self.strat)
            col_scores.append((score, col))
        random.shuffle(col_scores)
        sc = sorted(col_scores, key=itemgetter(0), reverse=True)
        #print 'Col Scores', str(sc)
        column = sc[0][1]
        #print column
        return column