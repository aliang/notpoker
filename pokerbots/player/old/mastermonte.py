from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Post, Show, Deal
from random import sample
from numpy import *

class MasterMonte:
    def __init__(self):
        """This is a template for writing our own bots. (The other template is
        the template they included)
        """
        # my name
        self.name = "MasterMonte"

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

        # my specific variables
        self.hand_counter = 0

    def respond(self):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically check/fold you
        """
        
        if not self.board.board:
            #self.evaluate_opponent()
            return self.preflop_strategy()
        elif self.board:
            if len(self.board.board) == 3:
                return self.flop_strategy()
            elif len(self.board.board) == 4:
                return self.turn_strategy()
            elif len(self.board.board) == 5:
                return self.river_strategy()

        # this is the default action, in case you forget to return something.
        # it's better than folding
        return Check()

    def evaluate_opponent(self):

        # only perform at the beginning of the next hand
        if self.hands_played > 2:           
            if self.hand_counter != self.hands_played:
                self.hand_counter = self.hands_played
                for play in self.last[0]:
                    print play[1]
                #print filter(lambda x: x[0]==self.opponent['name'], self.last[0])
                #print filter(lambda x: x[0]=='Dealer',self.last[0])
    
    def preflop_strategy(self):
        """
        Returns an action before the flop, based on the table and the player
        """
        
        # This calls Zach's preflop evaluator
        preflop_percentile = self.evaluate_preflop()

        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

        for action in self.legal:
            if isinstance(action, Bet):
                if preflop_percentile < 1:
                    value_bet = int(round(potodds_ratio*preflop_percentile*pot_size/(1-preflop_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2*self.pip
                if preflop_percentile < 1:
                    value_bet = int(round(potodds_ratio*preflop_percentile*pot_size/(1-preflop_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2*chips_to_add:
                        return Raise(value_bet + self.pip)
                    elif value_bet >= chips_to_add:
                        return Call()
                    else:
                        return Fold()
                else:
                    return Raise(self.stack + self.pip) # go all-in

        # if something screws up, try checking
        return Check()
    
    def flop_strategy(self):
        """
        Returns an action after the flop, based on the table and the player
        """
        # This calls Zach's flop evaluator
        flop_percentile = self.evaluate_flop()

        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

        for action in self.legal:
            if isinstance(action, Bet):
                if flop_percentile < 1:
                    value_bet = int(round(potodds_ratio*flop_percentile*pot_size/(1-flop_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2*self.pip
                if flop_percentile < 1:
                    value_bet = int(round(potodds_ratio*flop_percentile*pot_size/(1-flop_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2*chips_to_add:
                        return Raise(value_bet + self.pip)
                    elif value_bet >= chips_to_add:
                        return Call()
                    else:
                        return Fold()
                else:
                    return Raise(self.stack + self.pip) # go all-in

        # if something screws up, try checking
        return Check()
    
    def turn_strategy(self):
        """
        Returns an action after the turn, based on the table and the player
        """
        # This calls Zach's turn evaluator
        turn_percentile = self.evaluate_turn()
        
        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

        for action in self.legal:
            if isinstance(action, Bet):
                if turn_percentile < 1:
                    value_bet = int(round(potodds_ratio*turn_percentile*pot_size/(1-turn_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2*self.pip
                if turn_percentile < 1:
                    value_bet = int(round(potodds_ratio*turn_percentile*pot_size/(1-turn_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2*chips_to_add:
                        return Raise(value_bet + self.pip)
                    elif value_bet >= chips_to_add:
                        return Call()
                    else:
                        return Fold()
                else:
                    return Raise(self.stack + self.pip) # go all-in

        # if something screws up, try checking
        return Check()
    
    def river_strategy(self):
        """
        Returns an action after the river, based on the table and the player
        """
        # This calls Zach's river evaluator
        river_percentile = self.evaluate_river()
        
        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

        for action in self.legal:
            if isinstance(action, Bet):
                if river_percentile < 1:
                    value_bet = int(round(potodds_ratio*river_percentile*pot_size/(1-river_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2*self.pip
                if river_percentile < 1:
                    value_bet = int(round(potodds_ratio*river_percentile*pot_size/(1-river_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2*chips_to_add:
                        return Raise(value_bet + self.pip)
                    elif value_bet >= chips_to_add:
                        return Call()
                    else:
                        return Fold()
                else:
                    return Raise(self.stack + self.pip) # go all-in

        # if something screws up, try checking
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

        # total possible hands opponent can have
        total_iterations = 100
        # number of hands in which I beat/tie opponent (to be counted)
        beat_opponent = 0.0

        # list of all 52 cards by rank and suit
        available_ranks = tile(xrange(2,14+1),4)
        available_suits = tile(xrange(1,4+1),13)

        # remove the cards already in my hand or on table
        my_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                            self.board.board[2].rank],int)
        my_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                            self.board.board[2].suit],int)
        for i in xrange(52,1-1,-1):
            if sum((my_ranks == available_ranks[i-1]) * (my_suits == available_suits[i-1])):
                available_ranks = delete(available_ranks,i-1)
                available_suits = delete(available_suits,i-1)

        # Monte Carlo sampling of opponent's hand, turn, and river
        for i in xrange(1,total_iterations+1):
            random_cards = sample(xrange(0,47),4)
            opponent_cards = random_cards[:2]
            table_cards = random_cards[2:]

            my_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                              self.board.board[2].rank,available_ranks[table_cards[0]],available_ranks[table_cards[1]]],int)
            my_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                              self.board.board[2].suit,available_suits[table_cards[0]],available_suits[table_cards[1]]],int)
            
            opponent_ranks = array([available_ranks[opponent_cards[0]],available_ranks[opponent_cards[1]],
                                    self.board.board[0].rank,self.board.board[1].rank,self.board.board[2].rank,
                                    available_ranks[table_cards[0]],available_ranks[table_cards[1]]],int)
            opponent_suits = array([available_suits[opponent_cards[0]],available_suits[opponent_cards[1]],
                                    self.board.board[0].suit,self.board.board[1].suit,self.board.board[2].suit,
                                    available_suits[table_cards[0]],available_suits[table_cards[1]]],int)

            my_strength = self.evaluate_hand(my_ranks,my_suits)
            opponent_strength = self.evaluate_hand(opponent_ranks,opponent_suits)
            strength_diff = my_strength - opponent_strength
            if len(nonzero(strength_diff!=0)[0]):
                if sign(strength_diff[nonzero(strength_diff!=0)[0][0]]) > 0:
                    beat_opponent = beat_opponent+1     # my hand is better than opponent's
            else:
                beat_opponent = beat_opponent+0.5     #my hand and opponent's are the same

        # this is the fraction of hands you beat
        flop_percentile = beat_opponent/total_iterations
                       
        return flop_percentile

    def evaluate_turn(self):
        """
        Return the fraction of other hands you beat after the turn
        (assuming opponent has any two cards).
        """
        # total possible hands opponent can have
        total_iterations = 100
        # number of hands in which I beat/tie opponent (to be counted)
        beat_opponent = 0.0

        # list of all 52 cards by rank and suit
        available_ranks = tile(xrange(2,14+1),4)
        available_suits = tile(xrange(1,4+1),13)

        # remove the cards already in my hand or on table
        my_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                            self.board.board[2].rank,self.board.board[3].rank],int)
        my_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                            self.board.board[2].suit,self.board.board[3].suit],int)
        for i in xrange(52,1-1,-1):
            if sum((my_ranks == available_ranks[i-1]) * (my_suits == available_suits[i-1])):
                available_ranks = delete(available_ranks,i-1)
                available_suits = delete(available_suits,i-1)

        # Monte Carlo sampling of opponent's hand, turn, and river
        for i in xrange(1,total_iterations+1):
            random_cards = sample(xrange(0,46),3)
            opponent_cards = random_cards[:2]
            table_cards = random_cards[2]
            
            my_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                              self.board.board[2].rank,self.board.board[3].rank,available_ranks[table_cards]],int)
            my_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                              self.board.board[2].suit,self.board.board[3].suit,available_suits[table_cards]],int)
            
            opponent_ranks = array([available_ranks[opponent_cards[0]],available_ranks[opponent_cards[1]],
                                    self.board.board[0].rank,self.board.board[1].rank,self.board.board[2].rank,
                                    self.board.board[3].rank,available_ranks[table_cards]],int)
            opponent_suits = array([available_suits[opponent_cards[0]],available_suits[opponent_cards[1]],
                                    self.board.board[0].suit,self.board.board[1].suit,self.board.board[2].suit,
                                    self.board.board[3].suit,available_suits[table_cards]],int)

            my_strength = self.evaluate_hand(my_ranks,my_suits)
            opponent_strength = self.evaluate_hand(opponent_ranks,opponent_suits)
            strength_diff = my_strength - opponent_strength
            if len(nonzero(strength_diff!=0)[0]):
                if sign(strength_diff[nonzero(strength_diff!=0)[0][0]]) > 0:
                    beat_opponent = beat_opponent+1     # my hand is better than opponent's
            else:
                beat_opponent = beat_opponent+0.5     #my hand and opponent's are the same

        # this is the fraction of hands you beat
        turn_percentile = beat_opponent/total_iterations
                       
        return turn_percentile
    
    def evaluate_river(self):
        """
        Return the fraction of other hands you beat after the river
        (assuming opponent has any two cards).
        """
        # total possible hands opponent can have
        total_iterations = 100
        # number of hands in which I beat/tie opponent (to be counted)
        beat_opponent = 0.0

        # list of all 52 cards by rank and suit
        available_ranks = tile(xrange(2,14+1),4)
        available_suits = tile(xrange(1,4+1),13)

        # remove the cards already in my hand or on table
        my_ranks = array([self.hand[0].rank,self.hand[1].rank,self.board.board[0].rank,self.board.board[1].rank,
                            self.board.board[2].rank,self.board.board[3].rank,self.board.board[4].rank],int)
        my_suits = array([self.hand[0].suit,self.hand[1].suit,self.board.board[0].suit,self.board.board[1].suit,
                            self.board.board[2].suit,self.board.board[3].suit,self.board.board[4].suit],int)
        for i in xrange(52,1-1,-1):
            if sum((my_ranks == available_ranks[i-1]) * (my_suits == available_suits[i-1])):
                available_ranks = delete(available_ranks,i-1)
                available_suits = delete(available_suits,i-1)

        # Monte Carlo sampling of opponent's hand, turn, and river
        for i in xrange(1,total_iterations+1):
            random_cards = sample(xrange(0,45),2)
            opponent_cards = random_cards
            
            opponent_ranks = array([available_ranks[opponent_cards[0]],available_ranks[opponent_cards[1]],
                                    self.board.board[0].rank,self.board.board[1].rank,self.board.board[2].rank,
                                    self.board.board[3].rank,self.board.board[4].rank],int)
            opponent_suits = array([available_suits[opponent_cards[0]],available_suits[opponent_cards[1]],
                                    self.board.board[0].suit,self.board.board[1].suit,self.board.board[2].suit,
                                    self.board.board[3].suit,self.board.board[4].suit],int)

            my_strength = self.evaluate_hand(my_ranks,my_suits)
            opponent_strength = self.evaluate_hand(opponent_ranks,opponent_suits)
            strength_diff = my_strength - opponent_strength
            if len(nonzero(strength_diff!=0)[0]):
                if sign(strength_diff[nonzero(strength_diff!=0)[0][0]]) > 0:
                    beat_opponent = beat_opponent+1     # my hand is better than opponent's
            else:
                beat_opponent = beat_opponent+0.5     #my hand and opponent's are the same

        # this is the fraction of hands you beat
        river_percentile = beat_opponent/total_iterations
                       
        return river_percentile


    def evaluate_hand(self,card_ranks,card_suits):
        """
        Return the strength of a given 5-7 card hand in hand_strength form
        """

        # A is the ranks of the cards (2-14)
        A = card_ranks
        # B is the suits of the cards (1-4)
        B = card_suits

        suit_frequency = zeros(4,int)
        for i in xrange(0,4):
            suit_frequency[i] = sum(B==i+1)
        sorted_ranks = flipud(sort(A))

        # look for straight-flush
        if max(suit_frequency) > 4:
            flush_suit = xrange(1,4+1)[nonzero(suit_frequency>4)[0][0]]
            suited_cards = A*(B==flush_suit)
            for i in sorted_ranks[4:]:
                if sum(suited_cards==i)*sum(suited_cards==i+1)*sum(suited_cards==i+2)*sum(suited_cards==i+3)*sum(suited_cards==i+4):
                    hand_strength = array([9,i+4,0,0,0,0])
                    return hand_strength
            # look for wheel-flush
            if sum(suited_cards==14)*sum(suited_cards==2)*sum(suited_cards==3)*sum(suited_cards==4)*sum(suited_cards==5):
                return array([9,5,0,0,0,0])

        rank_frequency = zeros(13,int)
        for i in A:
            rank_frequency[i-2] = rank_frequency[i-2]+1
        sorted_rank_frequency = flipud(sort(rank_frequency))

        # look for quad
        if sorted_rank_frequency[0] == 4:
            quad_card = array(xrange(2,14+1))[nonzero(rank_frequency==4)[0][0]]
            kickers = xrange(2,14+1)*(rank_frequency>0)*(rank_frequency<4)
            return array([8,quad_card,max(kickers),0,0,0])

        # look for full-house
        if sorted_rank_frequency[0] == 3:
            trip_cards = array(xrange(2,14+1))[nonzero(rank_frequency==3)[0]]
            high_trip = max(trip_cards)
            if sorted_rank_frequency[1] > 1:
                high_pair = max(array(xrange(2,14+1))[nonzero(rank_frequency>1)[0]*(nonzero(rank_frequency>1)[0]!=high_trip-2)])
                return array([7,high_trip,high_pair,0,0,0])

        # look for flush
        if max(suit_frequency) > 4:
            suited_cards = flipud(sort(suited_cards))
            return array([6,suited_cards[0],suited_cards[1],suited_cards[2],suited_cards[3],suited_cards[4]])
            
        # look for straight
        for i in sorted_ranks[4:]:
            if sum(A==i)*sum(A==i+1)*sum(A==i+2)*sum(A==i+3)*sum(A==i+4):
                return array([5,i+4,0,0,0,0])
        # look for wheel
        if sum(A==14)*sum(A==2)*sum(A==3)*sum(A==4)*sum(A==5):
            return array([5,5,0,0,0,0])

        # look for trip
        if sorted_rank_frequency[0] == 3:
            kickers = flipud(sort(xrange(2,14+1)*(rank_frequency==1)))
            return array([4,high_trip,kickers[0],kickers[1],0,0])

        # look for two-pair
        if sorted_rank_frequency[0] == 2:
            pair_cards = array(xrange(2,14+1))[nonzero(rank_frequency==2)[0]]
            # look for 2-pair
            if sorted_rank_frequency[1] == 2:
                sorted_pairs = flipud(sort(pair_cards))
                high_pair = sorted_pairs[0]
                next_pair = sorted_pairs[1]
                kicker = max(array(xrange(2,14+1))[nonzero(rank_frequency>0)[0]*(nonzero(rank_frequency>0)[0]!=high_pair-2)*(nonzero(rank_frequency>0)[0]!=next_pair-2)])
                return array([3,high_pair,next_pair,kicker,0,0])
            # just a pair
            else:
                kickers = xrange(2,14+1)*(rank_frequency==1)
                kickers = flipud(sort(kickers))
                return array([2,pair_cards,kickers[0],kickers[1],kickers[2],0])

        # high-card
        kickers = flipud(sort(card_ranks))
        return array([1,kickers[0],kickers[1],kickers[2],kickers[3],kickers[4]])
