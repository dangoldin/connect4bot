import json
import utils

class strategy:
    def __init__(self, player):
        self.player = player
        self.utils = utils.utils()
    
    def getPlayer(self):
        return self.player
    
    def getBoard(self, json_str):
        data = json.loads(json_str)
        return data['board']
       
    def getMoveJSON(self, json_str):
        board = self.getBoard(json_str)
        return self.getMove(board)