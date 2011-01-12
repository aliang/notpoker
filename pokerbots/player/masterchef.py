from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint
from numpy import *

class MasterChef:
    def __init__(self):
        """This is a template for writing our own bots. (The other template is
        the template they included)
        """
        # my name
        self.name = "MasterChef"

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

        if not self.board.board:
            return self.preflop_strategy()
        elif self.board:
            if len(self.board.board) == 3:
                return self.flop_strategy()
            elif len(self.board.board) == 4:
                # replace with your turn logic
                return self.turn_strategy()
            elif len(self.board.board) == 5:
                # replace with your river logic
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
        A = self.evaluate_flop()
        return Check()
    
    def turn_strategy(self):
        """
        Returns an action after the turn, based on the table and the player
        """
        A = self.evaluate_turn()
        return Check()
    
    def river_strategy(self):
        """
        Returns an action after the river, based on the table and the player
        """
        A = self.evaluate_river()
        return Check()
    
    def evaluate_preflop(self):
        """
        Return the fraction of other hands you beat before the flop
        (assuming opponent has any two cards).
        """
        # This is Zach's pre-flop evaluator
        preflop_order_matrix = array([[87,169,168,166,167,165,159,149,135,121,105,86,59],
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
                          [46,38,35,30,31,24,21,18,13,11,10,8,1]])

        preflop_count_matrix = array([3,3,3,3,3,3,3,2,3,2,2,6,2,6,6,2,3,2,6,2,
                         2,2,6,2,6,6,3,2,2,2,2,6,6,2,2,6,2,2,6,6,
                         6,6,2,2,2,2,6,3,6,2,6,2,6,2,2,6,6,6,6,2,
                         2,6,2,2,2,3,2,6,6,6,2,2,2,6,2,2,6,6,6,6,
                         6,2,2,2,2,6,3,2,6,2,6,6,6,2,2,2,2,6,6,2,
                         6,6,2,2,6,2,6,2,6,2,6,6,2,2,2,6,6,2,2,6,
                         6,6,2,2,6,2,6,2,2,6,6,2,6,2,6,2,6,2,2,6,
                         6,2,2,6,6,2,2,6,6,2,6,2,6,6,2,2,6,2,6,6,
                         6,6,2,6,6,6,6,6,6])
        preflop_count_sum = 663.0

        sorted_rank = sorted([self.hand[0].rank,self.hand[1].rank])
        if self.hand[0].suit == self.hand[1].suit:
            preflop_order = preflop_order_matrix[sorted_rank[1]-2][sorted_rank[0]-2]
        else:
            preflop_order = preflop_order_matrix[sorted_rank[0]-2][sorted_rank[1]-2]

        # this is fraction of hands you beat
        preflop_percentile = 1 - sum(preflop_count_matrix[0:preflop_order-1])/preflop_count_sum
        
        return preflop_percentile

    def evaluate_flop(self):
        """
        Return the fraction of other hands you beat after the flop
        (assuming opponent has any two cards).
        """

        card_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                            self.board.board[2].rank])
        card_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                            self.board.board[2].suit])

        my_strength = self.evaluate_hand(card_ranks,card_suits)
        
        return 1

    def evaluate_turn(self):
        """
        Return the fraction of other hands you beat after the turn
        (assuming opponent has any two cards).
        """
        card_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                            self.board.board[2].rank,self.board.board[3].rank])
        card_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                            self.board.board[2].suit,self.board.board[3].suit])

        my_strength = self.evaluate_hand(card_ranks,card_suits)

        return 1

    def evaluate_river(self):
        """
        Return the fraction of other hands you beat after the river
        (assuming opponent has any two cards).
        """
        card_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                            self.board.board[2].rank,self.board.board[3].rank,self.board.board[4].rank])
        card_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                            self.board.board[2].suit,self.board.board[3].suit,self.board.board[4].suit])

        my_strength = self.evaluate_hand(card_ranks,card_suits)

        return 1

    def evaluate_hand(self,card_ranks,card_suits):
        """
        Return the strength of a given 5-7 card hand in hand_strength form
        """

        # A is the ranks of the cards (2-14)
        A = card_ranks
        # B is the suits of the cards (1-4)
        B = card_suits

        # initialize hand_strength to zeros
        hand_strength = zeros(6)
        
        # look for the wheel
        if sum(A==14)*sum(A==2)*sum(A==3)*sum(A==4)*sum(A==5):
            hand_strength = array([5,5,0,0,0,0])
        # look for higher straights
        for i in range(2,10+1):
            if sum(A==i)*sum(A==i+1)*sum(A==i+2)*sum(A==i+3)*sum(A==i+4):
                hand_strength = array([5,i+4,0,0,0,0])

        # look for flush and straight-flush
        suit_frequency = zeros(4)
        for i in range(0,4):
            suit_frequency[i] = sum(B==i+1)
        if max(suit_frequency) > 4:
            flush_suit = array(range(1,4+1))[nonzero(suit_frequency>4)[0][0]]
            suited_cards = A*(B==flush_suit)
            # look for wheel-flush
            if sum(suited_cards==14)*sum(suited_cards==2)*sum(suited_cards==3)*sum(suited_cards==4)*sum(suited_cards==5):
                hand_strength = array([9,5,0,0,0,0])
            # look for higher straight-flushes
            for i in range(2,10+1):
                if sum(suited_cards==i)*sum(suited_cards==i+1)*sum(suited_cards==i+2)*sum(suited_cards==i+3)*sum(suited_cards==i+4):
                    hand_strength = array([9,i+4,0,0,0,0])
            # if no straight flush, determine 
            if hand_strength[0] < 6:
                suited_cards = flipud(sort(suited_cards))
                hand_strength = array([6,suited_cards[0],suited_cards[1],suited_cards[2],suited_cards[3],suited_cards[4]])

        # look for pair, 2-pair, trips, full-house, and quad
        rank_frequency = zeros(13)
        for i in range(0,13):
            rank_frequency[i] = sum(A==i+2)
        sorted_rank_frequency = flipud(sort(rank_frequency))
        # look for quad
        if sorted_rank_frequency[0] == 4:
            quad_card = array(range(2,14+1))[nonzero(rank_frequency==4)[0][0]]
            kickers = range(2,14+1)*(rank_frequency>0)*(rank_frequency<4)
            hand_strength = array([8,quad_card,max(kickers),0,0,0])
        # look for trips
        elif sorted_rank_frequency[0] == 3:
            trip_cards = array(range(2,14+1))[nonzero(rank_frequency==3)[0]]
            high_trip = max(trip_cards)
            # look for full-house
            if sorted_rank_frequency[1] > 1:
                for i in range(0,13):
                    if rank_frequency[i] > 1 and i+2 != high_trip:
                        high_pair = i+2
                if hand_strength[0] < 7:
                    hand_strength = array([7,high_trip,high_pair,0,0,0])
            # just a trip
            else:
                kickers = range(2,14+1)*(rank_frequency==1)
                kickers = flipud(sort(kickers))
                if hand_strength[0] < 4:
                    hand_strength = array([4,high_trip,kickers[0],kickers[1],0,0])
        # look for pair and 2-pair
        elif sorted_rank_frequency[0] == 2:
            pair_cards = array(range(2,14+1))[nonzero(rank_frequency==2)[0]]
            # look for 2-pair
            if sorted_rank_frequency[1] == 2:
                sorted_pairs = flipud(sort(pair_cards))
                high_pair = sorted_pairs[0]
                next_pair = sorted_pairs[1]
                for i in range(0,13):
                    if rank_frequency[i] and i+2 != high_pair and i+2 != next_pair:
                        kicker = i+2
                if hand_strength[0] < 3:
                    hand_strength = array([3,high_pair,next_pair,kicker,0,0])
            # just a pair
            else:
                kickers = range(2,14+1)*(rank_frequency==1)
                kickers = flipud(sort(kickers))
                if hand_strength[0] < 2:
                    hand_strength = array([2,pair_cards,kickers[0],kickers[1],kickers[2],0])
        # just a high card
        else:
            kickers = flipud(sort(card_ranks))
            hand_strength = array([1,kickers[0],kickers[1],kickers[2],kickers[3],kickers[4]])
            

        return hand_strength 
