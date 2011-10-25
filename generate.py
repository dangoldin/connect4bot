from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import DBAdapters

import math, random, pickle, datetime
from c4 import c4
import utils
from strategies import dumb
from operator import itemgetter, attrgetter

ROUNDS = 20

utils = utils.utils()
#def gp_sqrt(a): return math.sqrt(abs(a))
def gp_add(a, b):
    return a + b
def gp_sub(a, b):
    return a - b
#def gp_mul(a, b):
#    return a * b
#def gp_div(a, b):
#    if b == 0:
#        return a
#    else:
#        return a/b
def gp_igt(a, b, c, d):
    if a > b:
        return c
    else:
        return d

def eval_func(chromosome):
    try:
        old_best_comp = compile(pickle.load(open('best.c4', 'rb')), "<string>", "eval")
    except:
        old_best_comp = None
    code_comp = chromosome.getCompiledCode()

    win = lose = tie = 0.0
    for rounds in range(ROUNDS):
        c = c4(rows=6,cols=7)
        rand_player = dumb.dumb(2)
        winner = 0
        turns = 0
        total_turns = c.rows * c.cols
        for i in range(c.rows * c.cols):
            winner = c.isWinner()
            if winner <> 0:
                break
            board_json = c.getBoard(is_json=True)
            board = c.getBoard(is_json=False)
            player = (i % 2) + 1
            if player == 1:
                col_scores = []
                for col in utils.getFreeCols(board):
                    aps, apo, eps, epo, nlt = utils.getStats(board,player,col)
                    score = eval(code_comp)
                    col_scores.append((score, col))
                random.shuffle(col_scores)
                sc = sorted(col_scores, key=itemgetter(0), reverse=True)
                #print 'Col Scores', str(sc)
                column = sc[0][1]
                c.move(player, column)
            else:
                if False: #old_best_comp is not None:
                    col_scores = []
                    for col in utils.getFreeCols(board):
                        aps, apo, eps, epo, nlt = utils.getStats(board,player,col)
                        score = eval(old_best_comp)
                        col_scores.append((score, col))
                    random.shuffle(col_scores)
                    sc = sorted(col_scores, key=itemgetter(0), reverse=True)
                    #print 'Col Scores', str(sc)
                    column = sc[0][1]
                else:
                    column = rand_player.getMove(board_json)
                c.move(player, column)
            turns += 1

        if winner == 1:
            win += 1.0 * total_turns/turns
        elif winner == 2:
            lose += 1.0 * total_turns/turns
        else:
            tie += 1
    
    return max(0,ROUNDS + win + 0.5 * tie - lose)

def save_best(gp_engine):
    best = gp_engine.bestIndividual()
    #print 'Individual: ' + str(dir(best))
    now = datetime.datetime.today()
    pickle.dump(best.getPreOrderExpression(), open('best.c4', 'wb'))
    pickle.dump(best.getPreOrderExpression(), open('best-%s.c4' % (now.strftime('%Y-%m-%d-%H-%M-%S')), 'wb'))
    return False

def main_run():
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=6, method="ramped")
    genome.evaluator += eval_func
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setParams(gp_terminals = ['aps', 'apo', 'nlt'], #['aps', 'apo', 'eps', 'epo', 'nlt'],
                 gp_function_prefix = "gp")
    ga.setMinimax(Consts.minimaxType["maximize"])
    ga.setGenerations(20)
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.25)
    ga.setPopulationSize(20)
    ga.stepCallback.set(save_best)
    #csvfile_adapter = DBAdapters.DBFileCSV()
    #ga.setDBAdapter(csvfile_adapter)
    ga.evolve(freq_stats=5)
    best = ga.bestIndividual()
    print best

if __name__ == "__main__":
    main_run()