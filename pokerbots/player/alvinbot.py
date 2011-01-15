from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint
from hand_evaluator import HandEvaluator

class AlvinBot:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "AlvinBot"
        # to keep hand_history
        self.hand_history = []

        # game state variables -- these are updated by the engine which has its
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving the remainder of the init as is
        self.hand = None # a tuple
        self.stack = None
        self.pip = None
        self.button = None
        self.opponent = None
        self.bb = None
        self.sb = None
        self.hands_played = None
        self.board = None # a Board object
        self.legal = None

    def respond(self):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically check/fold you
        """
        
        # self.last contains the last hand
        # define self.hand_history as [] in __init__
        # or you can't append to this list
        self.hand_history.append(self.last)
        
        # see other templates for a modular way of determining an action
        if not self.board.board:
            hand_data = HandEvaluator.evaluate_preflop_hand(self.hand)
        elif self.board:
            hand_data = HandEvaluator.evaluate_hand(self.board.cards + list(self.hand))
            if len(self.board.board) == 3:
                return Check()
            elif len(self.board.board) == 4:
                return Check()
            elif len(self.board.board) == 5:
                return Check()
        
        return Check()
    
    def preflop_strategy(self, hand_data):
        """
        Returns an action before the flop, based on the table and the player
        """
        # This calls Zach's preflop evaluator
        preflop_percentile = hand_data['percentile']

        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

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
        
    def flop_strategy(self, hand_data):
        """
        Returns an action after the flop, based on the table and the player
        """
        # This calls Zach's flop evaluator
        flop_percentile = hand_data['percentile']

        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

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
                chips_to_add = pot_size - 2*self.pip
                if flop_percentile < 1:
                    value_bet = int(round(potodds_ratio * flop_percentile * pot_size/(1 - flop_percentile)))
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

    def turn_strategy(self, hand_data):
        """
        Returns an action after the turn, based on the table and the player
        """
        # This calls Zach's turn evaluator
        turn_percentile = hand_data['percentile']

        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

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
                chips_to_add = pot_size - 2*self.pip
                if turn_percentile < 1:
                    value_bet = int(round(potodds_ratio * turn_percentile * pot_size / (1 - turn_percentile)))
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

    def river_strategy(self, hand_data):
        """
        Returns an action after the river, based on the table and the player
        """
        # This calls Zach's river evaluator
        river_percentile = hand_data['percentile']

        potodds_ratio = 0.50
        pot_size = 800 - self.opponent['stack'] - self.stack

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
                chips_to_add = pot_size - 2*self.pip
                if river_percentile < 1:
                    value_bet = int(round(potodds_ratio * river_percentile * pot_size / (1 - river_percentile)))
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