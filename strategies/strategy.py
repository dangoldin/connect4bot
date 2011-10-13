import json
import utils

class strategy:
    def __init__(self, player):
        self.player = player
        self.utils = utils.utils()
    
    def getPlayer(self):
        return self.player
    
    def getBoard(self, board_json):
        return json.loads(board_json)
    
    