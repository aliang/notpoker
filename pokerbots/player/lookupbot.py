from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Card
from random import randint
from hand_evaluator import HandEvaluator

class LookupBot:
    """
    This is the new template bot.
    Copy this file to a new bot, then override __init__ and respond
    """
    def __init__(self):
        # my name
        self.name = "LookupBot"

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
            hand_data = HandEvaluator.evaluate_preflop_hand(self.hand)
        elif self.board:
            hand_data = HandEvaluator.evaluate_hand(self.board.cards + list(self.hand))
            if len(self.board.board) == 3:
                return Check()
            elif len(self.board.board) == 4:
                return Check()
            elif len(self.board.board) == 5:
                return Check()
        
        # always return Check() as last resort, because it beats Fold()
        return Check()