from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint
from hand_evaluator import HandEvaluator

class AlvinBot:
    def __init__(self):
        """
        This bot is currently MasterChef50, but using Alvin's fast hand
        evaluator. It plays 50 games against itself in under 3 seconds.
        """
        # my name
        self.name = "AlvinBot"
        # to keep hand_history
        self.hand_counter = 0
        # to store percentiles for this hand
        self.percentiles = {}

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
        
        if self.hands_played != self.hand_counter:
            self.hand_counter = self.hands_played
            # reset stuff
            self.percentiles = {}
        
        # self.last contains the last hand
        # define self.hand_history as [] in __init__
        # or you can't append to this list
        # self.hand_history.append(self.last)
        
        # see other templates for a modular way of determining an action
        if not self.board.board:
            self.percentiles['preflop'] = HandEvaluator.evaluate_preflop_hand(self.hand)
            return self.preflop_strategy()
        elif self.board:
            if len(self.board.board) == 3:
                self.percentiles['flop'] = HandEvaluator.evaluate_hand(list(self.hand) + self.board.cards)
                return Check()
            elif len(self.board.board) == 4:
                self.percentiles['turn'] = HandEvaluator.evaluate_hand(list(self.hand) + self.board.cards)
                return Check()
            elif len(self.board.board) == 5:
                self.percentiles['river'] = HandEvaluator.evaluate_hand(list(self.hand) + self.board.cards)
                return Check()
        
        return Check()
    
    def preflop_strategy(self):
        """
        Returns an action before the flop, based on the table and the player
        """
        preflop_percentile = self.percentiles['preflop']

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