from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint
from hand_evaluator import HandEvaluator

class VivekBot:
    def __init__(self):
        """
        This bot is currently MasterChef50, but using Alvin's fast hand
        evaluator. It plays 50 games against itself in under 3 seconds.
        """
        # my name
        self.name = "VivekBot"
        # to keep hand_history
        self.hand_counter = 0
        # to store percentiles for this hand
        self.percentiles = {}
        # to store best estimates of opponent's percentiles
        self.opponent_percentiles = {}

        # game state variables -- these are updated by the engine which has its
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving the remainder of the init as is
        self.hand = None # a tuple
        self.stack = None # hopefully an integer
        self.pip = None # integer, stake in pot
        self.button = None # boolean, true if you have the button
        self.opponent = None # dictionary with 'pip', 'button', 'name', 'stack' for opponent
        self.bb = None # size of current big blind
        self.sb = None # size of current small blind
        self.hands_played = None # number of hands played
        self.board = None # a Board object
        self.legal = None # list of allowed actions, e.g. [Raise(8), Call(), Fold()]

        # state variables
        self.potodds_ratio = 0.5
        self.opponent_bet_history = zeros(0)

    def respond(self):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically check/fold you
        """
        debug=True;

        if debug:
            print(self.name)
            print('self.hand',self.hand)
            print('self.stack',self.stack)
            print('self.pip',self.pip)
            print('self.button',self.button)
            print('self.opponent',self.opponent)
            print('self.bb',self.bb)
            print('self.sb',self.sb)
            print('self.hands_played',self.hands_played)
            print('self.board',self.board)
            print('self.legal',self.legal)
            print('self.pot',self.pot)
            ok = raw_input('press enter\n');
            
        if self.hands_played != self.hand_counter:
            self.hand_counter = self.hands_played
            # reset stuff
            self.percentiles = {}
            self.opponent_percentiles = {}
            self.evaluate_opponent()
        
        # self.last contains the last hand
        # define self.hand_history as [] in __init__
        # or you can't append to this list
        # self.hand_history.append(self.last)
        
        # see other templates for a modular way of determining an action
        if not self.board.board:
            if 'preflop' not in self.percentiles:
                self.percentiles['preflop'] = HandEvaluator.evaluate_hand(self.hand)
            return self.preflop_strategy()
        elif self.board:
            if len(self.board.board) == 3:
                if 'flop' not in self.percentiles:
                    self.percentiles['flop'] = HandEvaluator.evaluate_hand(self.hand, self.board.cards)
                return self.flop_strategy()
            elif len(self.board.board) == 4:
                if 'turn' not in self.percentiles:
                    self.percentiles['turn'] = HandEvaluator.evaluate_hand(self.hand, self.board.cards)
                return self.turn_strategy()
            elif len(self.board.board) == 5:
                if 'river' not in self.percentiles:
                    self.percentiles['river'] = HandEvaluator.evaluate_hand(self.hand, self.board.cards)
                return self.river_strategy()
        
        return Check()
    
    def preflop_strategy(self):
        """
        Returns an action before the flop, based on the table and the player
        """
        preflop_percentile = self.percentiles['preflop']

        potodds_ratio = self.potodds_ratio
        pot_size = self.pot

        for action in self.legal:
            if isinstance(action, Bet):
                if preflop_percentile < 1:
                    value_bet = int(round(potodds_ratio * preflop_percentile * pot_size / (1 - preflop_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2 * self.pip
                if preflop_percentile < 1:
                    value_bet = int(round(potodds_ratio * preflop_percentile * pot_size / (1 - preflop_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2 * chips_to_add:
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
        flop_percentile = self.percentiles['flop']

        potodds_ratio = self.potodds_ratio
        pot_size = self.pot

        for action in self.legal:
            if isinstance(action, Bet):
                if flop_percentile < 1:
                    value_bet = int(round(potodds_ratio * flop_percentile * pot_size / (1 - flop_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2 * self.pip
                if flop_percentile < 1:
                    value_bet = int(round(potodds_ratio * flop_percentile * pot_size/(1 - flop_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2 * chips_to_add:
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
        turn_percentile = self.percentiles['turn']

        potodds_ratio = self.potodds_ratio
        pot_size = self.pot

        for action in self.legal:
            if isinstance(action, Bet):
                if turn_percentile < 1:
                    value_bet = int(round(potodds_ratio * turn_percentile * pot_size / (1 - turn_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2 * self.pip
                if turn_percentile < 1:
                    value_bet = int(round(potodds_ratio * turn_percentile * pot_size / (1 - turn_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2 * chips_to_add:
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
        river_percentile = self.percentiles['river']

        potodds_ratio = self.potodds_ratio
        pot_size = self.pot

        for action in self.legal:
            if isinstance(action, Bet):
                if river_percentile < 1:
                    value_bet = int(round(potodds_ratio * river_percentile * pot_size / (1 - river_percentile)))
                    if value_bet >= self.stack:
                        return Bet(self.stack)
                    elif value_bet > 0:
                        return Bet(value_bet)
                    else:
                        return Check()
                else:
                    return Bet(self.stack)  # go all-in
            elif isinstance(action, Raise):
                chips_to_add = pot_size - 2 * self.pip
                if river_percentile < 1:
                    value_bet = int(round(potodds_ratio * river_percentile * pot_size / (1 - river_percentile)))
                    if value_bet >= self.stack:
                        return Raise(self.stack + self.pip)
                    elif value_bet >= 2 * chips_to_add:
                        return Raise(value_bet + self.pip)
                    elif value_bet >= chips_to_add:
                        return Call()
                    else:
                        return Fold()
                else:
                    return Raise(self.stack + self.pip) # go all-in

        # if something screws up, try checking
        return Check()


    def evaluate_opponent(self):
        
        if self.hands_played >= 1:           
            last_pot = 0.0
            self_bet_for_round = 0
            opponent_bet_for_round = 0
            community_ranks = zeros(0,int)
            community_suits = zeros(0,int)

            # obtain opponent's betting behavior from the previous round, and determine strength of hand if there's a showdown
            # 
            for play in self.last[1]:
                if play[0] == self.name:
                    if isinstance(play[1],Post):
                        last_pot = last_pot + play[1].amount
                        self_bet_for_round = play[1].amount
                    elif isinstance(play[1],Bet):
                        last_pot = last_pot + play[1].amount
                        self_bet_for_round = play[1].amount
                    elif isinstance(play[1],Raise):
                        last_pot = last_pot - self_bet_for_round + play[1].amount
                        self_bet_for_round = play[1].amount
                    elif isinstance(play[1],Call):
                        last_pot = last_pot + opponent_bet_for_round - self_bet_for_round
                        self_bet_for_round = opponent_bet_for_round
                elif play[0] == self.opponent['name']:
                    strength_of_bet = zeros(0)
                    if isinstance(play[1],Post):
                        last_pot = last_pot + play[1].amount
                        opponent_bet_for_round = play[1].amount
                    elif isinstance(play[1],Bet):
                        last_pot = last_pot + play[1].amount
                        opponent_bet_for_round = play[1].amount
                        strength_of_bet = play[1].amount/last_pot
                    elif isinstance(play[1],Raise):
                        last_pot = last_pot - opponent_bet_for_round + play[1].amount
                        strength_of_bet = (play[1].amount - opponent_bet_for_round)/last_pot
                        opponent_bet_for_round = play[1].amount
                    elif isinstance(play[1],Call):
                        last_pot = last_pot + self_bet_for_round - opponent_bet_for_round
                        strength_of_bet = (self_bet_for_round - opponent_bet_for_round)/last_pot
                        opponent_bet_for_round = self_bet_for_round
                    elif isinstance(play[1],Check):
                        strength_of_bet = 0.0
                    elif isinstance(play[1],Show):
                        opponent_ranks = array([play[1].hand[0].rank,play[1].hand[1].rank])
                        opponent_suits = array([play[1].hand[0].suit,play[1].hand[1].suit])
                        strength_of_hand = self.percentile_of_hand(opponent_ranks,opponent_suits,
                                                                   community_ranks,community_suits)

                        HandEvaluator.evaluate_hand(play[1].hand, self.board.cards)
                        
                        #print strength_of_hand
                    self.opponent_bet_history = append(self.opponent_bet_history,strength_of_bet)
                    #print 'mean'
                    #print mean(self.opponent_bet_history)
                    #print 'std'
                    #print std(self.opponent_bet_history)
                elif play[0] == 'Dealer':
                    # Determine what the cards are if all five are out -- prepare for showdown
                    if len(play[1].cards) == 20:
                        community_ranks = append(community_ranks,self.parse_ranks(play[1].cards))
                        community_suits = append(community_suits,self.parse_suits(play[1].cards))                            
                    self_bet_for_round = 0
                    opponent_bet_for_round = 0
