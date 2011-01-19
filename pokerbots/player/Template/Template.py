from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

class Template(object):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # game state variables -- these are updated by the engine which
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving their init as is
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
        self.actions = None
        self.last = None
        self.pot = None
        self.time = None
        self.unlimited = True
        
        self.name = "Template"

    def respond(self):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically fold you
        """

        for action in self.legal:
            if isinstance(action, Raise):
                return Raise(self.pip + self.stack)
            return Call()

        for action in self.legal:
            if isinstance(action, Bet):
                if randint(0, 100) < 35:
                    return Bet(self.stack/2)
            return Check()

        return Fold()


    def reset(self, won, last_hand):
        """Reset accepts a boolean indicating whether you won a match and
        provides the last hand if you want to update any statistics from it
        """
        pass
