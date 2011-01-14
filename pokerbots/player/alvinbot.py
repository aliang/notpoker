from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

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
        
        # self.last contains the last hand
        # define self.hand_history as [] in __init__
        # or you can't append to this list
        self.hand_history.append(self.last)
        
        # see other templates for a modular way of determining an action
        
        return Check()