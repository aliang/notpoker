from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

class NotPokerTemplate:
    def __init__(self):
        """This is a template for writing our own bots. (The other template is
        the template they included)
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

        if not self.board:
            print "preflop"
            return self.preflop_strategy()
        elif self.board:
            if len(self.board) == 3:
                print "flopped"
                return self.flop_strategy()
            elif len(self.board) == 4:
                # replace with your turn logic
                print "turn"
                return self.turn_strategy()
            elif len(self.board) == 5:
                # replace with your river logic
                print "river"
                return self.river_strategy()

        # this is the default action, in case you forget to return something.
        # it's better than folding
        return Check()
        
    def preflop_strategy(self):
        """
        Returns an action before the flop, based on the table and the player
        """
        # This calls Zach's evaluator
        print self.evaluate_preflop()
        return Check()
    
    def flop_strategy(self):
        """
        Returns an action after the flop, based on the table and the player
        """
        return Check()
    
    def turn_strategy(self):
        """
        Returns an action after the turn, based on the table and the player
        """
        return Check()
    
    def river_strategy(self):
        """
        Returns an action after the river, based on the table and the player
        """
        return Check()
    
    def evaluate_preflop(self):
        """
        Return the fraction of other hands you beat before the flop
        (assuming opponent has any two cards).
        """
        # This is Zach's pre-flop evaluator
        preflop_order_matrix = [[87,169,168,166,167,165,159,149,135,121,105,86,59],
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

        preflop_count_matrix = [3,3,3,3,3,3,3,2,3,2,2,6,2,6,6,2,3,2,6,2,
                         2,2,6,2,6,6,3,2,2,2,2,6,6,2,2,6,2,2,6,6,
                         6,6,2,2,2,2,6,3,6,2,6,2,6,2,2,6,6,6,6,2,
                         2,6,2,2,2,3,2,6,6,6,2,2,2,6,2,2,6,6,6,6,
                         6,2,2,2,2,6,3,2,6,2,6,6,6,2,2,2,2,6,6,2,
                         6,6,2,2,6,2,6,2,6,2,6,6,2,2,2,6,6,2,2,6,
                         6,6,2,2,6,2,6,2,2,6,6,2,6,2,6,2,6,2,2,6,
                         6,2,2,6,6,2,2,6,6,2,6,2,6,6,2,2,6,2,6,6,
                         6,6,2,6,6,6,6,6,6]
        preflop_count_sum = 663.0

        sorted_rank = sorted([self.hand[0].rank,self.hand[1].rank])
        if self.hand[0].suit == self.hand[1].suit:
            preflop_order = preflop_order_matrix[sorted_rank[1]-2][sorted_rank[0]-2]
        else:
            preflop_order = preflop_order_matrix[sorted_rank[0]-2][sorted_rank[1]-2]

        if preflop_order == 1:
            preflop_percentile = 1
        else:
            # this is fraction of hands you beat
            preflop_percentile = 1 - sum(preflop_count_matrix[0:preflop_order-1])/preflop_count_sum
        # end Zach's preflop evaluator
        
        return preflop_percentile
    
    def evaluate_flop(self):
        """
        Return the fraction of other hands you beat after the flop
        (assuming opponent has any two cards)
        """
        return 1
        
    def evaluate_turn(self):
        """
        Return the fraction of other hands you beat after the turn
        (assuming opponent has any two cards)
        """
        return 1
    
    def evaluate_river(self):
        """
        Return the fraction of other hands you beat after the river
        (assuming opponent has any two cards)
        """
        return 1