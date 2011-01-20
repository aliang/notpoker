from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint
from hand_evaluator import HandEvaluator
from numpy import zeros

def VivekBotClassFactory(param1=0.9, param2=1, param3=0, param4=0.1):
    class VivekBot:
        def __init__(self):


        def reset(self, won, last_hand):
            """Reset accepts a boolean indicating whether you won a match and
            provides the last hand if you want to update any statistics from it
            """
            pass

    return VivekBot

# name of variable must be same as name of module
# pass your parameters to this function that acts as a class factory    
vivekbot = VivekBotClassFactory()

