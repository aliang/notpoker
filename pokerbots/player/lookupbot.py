from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Card
from random import randint
from operator import mul, __or__, __and__
from itertools import combinations
from lookup_tables import LookupTables

class LookupBot:
    def __init__(self):
        """This is a template for writing our own bots. (The other template is
        the template they included)
        """
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

        # this is the default action, in case you forget to return something.
        # it's better than folding
        return Check()

# These are some functions we're not using yet

def evaluate_hand(cards):
    """
    Return the rank and percentile of the best 5 card hand made from these
    cards, against an equivalent number of cards.
    Rank is given as a dict with:
        rank: rank within the 7462 equivalence classes,
        percentile: the percentile of hands you beat based on this rank
    """
    
    rank = 7463
    percentile = 0.0
    if len(cards) == 5:
        rank = evaluate_rank(cards)
        percentile = LookupTables.rank_to_percentile_5[rank - 1]
    elif len(cards) == 6:
        # evaluate all hands, choose the best one.
        # warning, don't pass too many cards here...
        possible_hands = combinations(cards, 5)
        rank = min(map(evaluate_rank, possible_hands))
        percentile = LookupTables.rank_to_percentile_6[rank - 1]
    elif len(cards) == 7:
        possible_hands = combinations(cards, 5)
        rank = min(map(evaluate_rank, possible_hands))
        percentile = LookupTables.rank_to_percentile_7[rank - 1]
    return {
        'rank': rank,
        'percentile': percentile
    }

def card_to_binary(card):
    """
    Convert the pokerbots.engine.game.Card represntation to a binary
    representation for use in hand evaluation
    """
    
    # This is Cactus Kev's algorithm, reimplemented in Python since we can't
    # use C libraries
    
    # First we need to generate the following representation
    # Bits marked x are not used.
    # xxxbbbbb bbbbbbbb cdhsrrrr xxpppppp

    # b is one bit flipped for A-2
    # c, d, h, s are flipped if you have a club, diamond, heart, spade
    # r is just the numerical rank in binary, with deuce = 0
    # p is the prime from LookupTable.primes corresponding to the rank,
    # in binary
    # Then shift appropriately to fit the template above
    
    b_mask = 1 << (14 + card.rank)
    cdhs_mask = 1 << (card.suit + 11)
    r_mask = (card.rank - 2) << 8
    p_mask = LookupTables.primes[card.rank - 2]
    # OR them together to get the final result
    return b_mask | r_mask | p_mask | cdhs_mask

# TODO: Return a class of hand too? Would be useful to see if we can make
# a draw or something.
def evaluate_rank(hand):
    """
    Find the rank of the hand amongst all 5-card hands.
    """
    
    # This implementation uses the binary representation from
    # card_to_binary
    
    # bh stands for binary hand
    bh = map(card_to_binary, hand)
    has_flush = reduce(__and__, bh, 0xF000)
    # This is a unique number based on the ranks if your cards,
    # assuming your cards are all different
    q = reduce(__or__, bh) >> 16
    if has_flush:
        # Look up the rank of this flush
        return LookupTables.flushes[q]
    else:
        possible_rank = LookupTables.unique5[q]
        if possible_rank != 0:
            return possible_rank
        else:
            # Compute the unique product of primes, because we have a pair
            # or trips, etc. Use the product to look up the rank.
            q = reduce(mul, map(lambda card: card & 0xFF, bh))
            # Here, use dict instead of sparse array (basically hashing)
            # I didn't bother using "perfect hash"
            return LookupTables.pairs.get(q)