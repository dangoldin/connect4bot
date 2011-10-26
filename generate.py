from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import DBAdapters

import math, random, pickle, datetime, json
from c4 import c4
import utils
from strategies import dumb
from operator import itemgetter, attrgetter
from gp_funcs import gp_add, gp_sub, gp_mul, gp_igt

ROUNDS = 8
ROWS = 6
COLS = 7

utils = utils.utils()

def eval_func(chromosome):
    try:
        old_best_comp = compile(pickle.load(open('best.c4', 'rb')), "<string>", "eval")
    except:
        old_best_comp = None
    code_comp = chromosome.getCompiledCode()

    win = lose = tie = 0.0
    for rnd in range(ROUNDS):
        c = c4(rows=ROWS,cols=COLS)
        if rnd % 2 == 0:
            other_player = dumb.url(1,'http://dl.no.de/ai/twostep/move')
        else:
            other_player = dumb.url(2,'http://dl.no.de/ai/twostep/move')
        winner = 0
        turns = 0
        total_turns = c.rows * c.cols
        for i in range(total_turns):
            winner = c.isWinner()
            if winner <> 0:
                break
            board = c.getBoard(is_json=False)
            player = (i % 2) + 1
            # Train if we're not the genetic player
            if other_player.getPlayer() == player:
                json_state = json.dumps( { "rows":ROWS,
                                           "cols":COLS,
                                           "board":board,
                                           "currentTurn":player,
                                           "moveNumber":i} )
                column = other_player.getMoveJSON(json_state)
            else: # Otherwise let's eval and see what we get
                col_scores = []
                for col in utils.getFreeCols(board):
                    const, aps, apo, nlts, nlto, nr = utils.getStats(board,player,col)
                    score = eval(code_comp)
                    col_scores.append((score, col))
                random.shuffle(col_scores)
                sc = sorted(col_scores, key=itemgetter(0), reverse=True)
                #print 'Col Scores', str(sc)
                column = sc[0][1]
            c.move(player, column)            
            # This is to compete against self, to do later
            #if False: #old_best_comp is not None:
            #    col_scores = []
            #    for col in utils.getFreeCols(board):
            #        aps, apo, nlts, nlto, nr = utils.getStats(board,player,col)
            #        score = eval(old_best_comp)
            #        col_scores.append((score, col))
            #    random.shuffle(col_scores)
            #    sc = sorted(col_scores, key=itemgetter(0), reverse=True)
            #    #print 'Col Scores', str(sc)
            #    column = sc[0][1]
            turns += 1

        if winner == 0:
            tie += 1.0
        elif winner == other_player.getPlayer():
            lose += 1.0
        else:
            win += 1.0
    
    return (win + tie * 0.5)/ROUNDS

def save_best(gp_engine):
    best = gp_engine.bestIndividual()
    #print 'Individual: ' + str(dir(best))
    now = datetime.datetime.today()
    print 'Time now: %s' % now.strftime('%Y-%m-%d-%H-%M-%S')
    pickle.dump(best.getPreOrderExpression(), open('best.c4', 'wb'))
    pickle.dump(best.getPreOrderExpression(), open('best-%s.c4' % (now.strftime('%Y-%m-%d-%H-%M-%S')), 'wb'))
    return False

def main_run():
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=4, method="ramped")
    genome.evaluator += eval_func
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setParams(gp_terminals = ['const', 'aps', 'apo', 'nlts', 'nlto', 'nr'], #['aps', 'apo', 'nlt'], #['aps', 'apo', 'eps', 'epo', 'nlt'],
                 gp_function_prefix = "gp")
    ga.setMinimax(Consts.minimaxType["maximize"])
    ga.setGenerations(200)
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.25)
    ga.setPopulationSize(200)
    ga.stepCallback.set(save_best)
    csvfile_adapter = DBAdapters.DBFileCSV()
    ga.setDBAdapter(csvfile_adapter)
    ga.evolve(freq_stats=1)
    best = ga.bestIndividual()
    print best

if __name__ == "__main__":
    main_run()