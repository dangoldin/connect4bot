import random, requests, json
from strategy import strategy

class dumb(strategy):
    
    def getMove(self, board):
        cols, rows = self.utils.getBoardDims(board)
        valid_cols = [i for i, col in enumerate(board) if col.count(0) > 0]
        column = random.choice(valid_cols)
        return column

class url(strategy):

    def __init__(self, player, url):
        strategy.__init__(self,player)
        self.url = url

    def getMoveJSON(self, json_str):
        #print json_str
        r = requests.post(self.url, data = json_str, headers={'Content-Type': 'application/json'})
        data = json.loads(r.content)
        #print data
        return int(data['move'])