#!/usr/bin/python

import json as simplejson, sys, time, random
from subprocess import check_output
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from strategies import genetic

global engine_path
global millis_per_move
global moves
moves = []

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        raise Exception("Not Supported")

    def do_POST(self):
        self.rfile.readline() # Skip header
        post_body = self.rfile.readline()
        data = simplejson.loads(post_body)
        
        #strats = ['best-2011-10-24-16-47-58.c4', 'best-2011-10-24-16-47-39.c4', 'best-2011-10-24-16-48-38.c4', 'best-2011-10-24-16-48-09.c4']
        strats = ['best-2011-10-24-16-48-26.c4',]
        random.shuffle(strats)
        
        strat = genetic.genetic(int(data['currentTurn']), strats[0])
        move = strat.getMove(data['board'])

        #move = get_move(data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write('{"move":%d}' % move)

"""
def get_move(data):
    set_prev_moves(data)
    move = find_best_move()
    moves.append(move)
    return move

def find_best_move():
    global moves
    global millis_per_move
    args = [engine_path, millis_per_move] + moves
    out = check_output(map(str, args)) 
    assert(out.count("\n") == 1) 
    return int(out)    

def set_prev_moves(data):
    global moves
    if data["moveNumber"] < 2:
        moves = []
    if data["moveNumber"] > 0:
        moves.append(data["lastMove"]["col"])

    print " ".join(str(move) for move in moves)
"""

def serve(port):
    try:
        server = HTTPServer(('',port), MyHandler)
        print 'Starting server...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server...'
        server.socket.close()

"""
def validate_and_store_engine(engine):
    global engine_path
    engine_path = engine

    try:
        find_best_move()
    except:
        print "Engine executable at %s does not exist or is not valid" % engine
        exit(-1)

def validate_and_store_millis(millis):
    assert(millis > 0)

    global millis_per_move
    millis_per_move = millis
"""
    
if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
        #engine = sys.argv[1]
        #port = int(sys.argv[2])
        #millis = int(sys.argv[3])
    except:
        print "Usage: server.py <path_to_engine> <port> <max_millis_per_move>"    
        exit(-1)

    #validate_and_store_millis(millis)
    #validate_and_store_engine(engine)

    serve(port)