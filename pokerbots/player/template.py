from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

class Template:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "testbot"

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
        for action in self.legal:
            if isinstance(action, Raise):
                if self.hand[0].rank == self.hand[1].rank:
                    return Raise(self.stack + self.pip)
                return Call()
            if isinstance(action, Bet):
                if randint(0, 100) < 35:
                    return Bet(self.stack/2)
                else
                    return Check()

        return Call()