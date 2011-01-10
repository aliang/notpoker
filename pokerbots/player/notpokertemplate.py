from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

class NotPokerTemplate:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "NotPokerTemplateBot"

        # game state variables -- these are updated by the engine which has its
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving the remainder of the init as is
        self.hand = None
        self.stack = None
        self.pip = None
        self.button = None
        self.opponent = None
        self.bb = None
        self.sb = None
        self.hands_played = None
        self.board = None
        self.legal = None

    def respond(self):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically check/fold you
        """
        
        # This is Zach's pre-flop evaluator
        preflop_matrix = [[87,169,168,166,167,165,159,149,135,121,105,86,59],
                          [163,66,164,161,162,160,157,144,131,116,98,80,53],
                          [158,150,48,153,154,151,148,140,125,111,93,74,49],
                          [155,146,136,27,145,141,137,130,122,107,89,69,41],
                          [156,147,138,128,17,133,127,120,112,102,81,62,42],
                          [152,143,134,124,115,9,117,109,101,92,77,58,36],
                          [142,139,129,119,110,100,7,99,91,79,68,51,32],
                          [132,126,123,113,103,94,83,6,78,70,56,40,25],
                          [118,114,108,106,96,84,73,64,5,57,47,33,19],
                          [104,97,95,90,85,75,65,55,45,4,39,26,15],
                          [88,82,76,72,67,61,52,43,34,28,3,23,14],
                          [71,63,60,54,50,44,37,29,22,20,16,2,12],
                          [46,38,35,30,31,24,21,18,13,11,10,8,1]]

        preflop_count = [3,3,3,3,3,3,3,2,3,2,2,6,2,6,6,2,3,2,6,2,
                         2,2,6,2,6,6,3,2,2,2,2,6,6,2,2,6,2,2,6,6,
                         6,6,2,2,2,2,6,3,6,2,6,2,6,2,2,6,6,6,6,2,
                         2,6,2,2,2,3,2,6,6,6,2,2,2,6,2,2,6,6,6,6,
                         6,2,2,2,2,6,3,2,6,2,6,6,6,2,2,2,2,6,6,2,
                         6,6,2,2,6,2,6,2,6,2,6,6,2,2,2,6,6,2,2,6,
                         6,6,2,2,6,2,6,2,2,6,6,2,6,2,6,2,6,2,2,6,
                         6,2,2,6,6,2,2,6,6,2,6,2,6,6,2,2,6,2,6,6,
                         6,6,2,6,6,6,6,6,6]
        count_sum = 663.0

        sorted_rank = sorted([self.hand[0].rank,self.hand[1].rank])
        if self.hand[0].suit == self.hand[1].suit:
            preflop_num = preflop_matrix[sorted_rank[1]-2][sorted_rank[0]-2]
        else:
            preflop_num = preflop_matrix[sorted_rank[0]-2][sorted_rank[1]-2]

        if preflop_num == 1:
            preflop_value = 1
        else:
            preflop_value = 1 - sum(preflop_count[0:preflop_num-1])/count_sum
        # end Zach's preflop evaluator

        if not self.board:
            # replace with your preflop logic
            print "preflop"
        
        if self.board:
            if len(self.board) == 3:
                # replace with your postflop logic
                print "flopped"
            elif len(self.board) == 4:
                # replace with your turn logic
                print "turn"
            elif len(self.board) == 5:
                # replace with your river logic
                print "river"

        # get rid of this line
        return Check()