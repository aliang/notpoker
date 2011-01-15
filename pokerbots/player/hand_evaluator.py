from lookup_tables import LookupTables
from itertools import combinations
from operator import mul, __or__, __and__

class HandEvaluator:
    def evaluate_preflop_hand(hand):
        """
        Return the fraction of other hands you beat before the flop
        (assuming opponent has any two cards).
        """
        if len(hand) != 2:
            return {
                'rank': 300,
                'percentile': 0
            }
        
        # This could be faster, but it doesn't run very much so whatever
        sorted_rank = sorted([hand[0].rank, hand[1].rank])
        if hand[0].suit == hand[1].suit:
            preflop_order = LookupTables.preflop_order_matrix[sorted_rank[1] - 2][sorted_rank[0] - 2]
        else:
            preflop_order = LookupTables.preflop_order_matrix[sorted_rank[0] - 2][sorted_rank[1] - 2]

        # this is fraction of hands you beat
        preflop_percentile = 1 - sum(LookupTables.preflop_count_matrix[0:preflop_order - 1]) / LookupTables.preflop_count_sum

        return {
            'rank': preflop_order,
            'percentile': preflop_percentile
        }
        

    # These are some functions we're not using yet
    def evaluate_hand(cards):
        """
        Return the rank and percentile of the best 5 card hand made from these
        cards, against an equivalent number of cards.
        Rank is given as a dict with:
            rank: rank within the 7462 equivalence classes,
            percentile: the percentile of hands you beat based on this rank
        """
        evaluate_rank = HandEvaluator.evaluate_rank
        
        # Default values in case we screw up
        rank = 7463
        percentile = 0.0
        if len(cards) == 5:
            rank = evaluate_rank(cards)
            # TODO: The space is different because only two cards vary.
            # The percentiles we look up are against any 5, 6, or 7 cards,
            # not against any 2.
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

    def card_to_binary_lookup(card):
        return LookupTables.card_to_binary[card.rank][card.suit]

    # TODO: Return a class of hand too? Would be useful to see if we can make
    # a draw or something.
    def evaluate_rank(hand):
        """
        Find the rank of the hand amongst all 5-card hands.
        """
        # This implementation uses the binary representation from
        # card_to_binary
        card_to_binary = HandEvaluator.card_to_binary_lookup

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
            # The q still works as a key if you have 5 unique cards,
            # so see if we can look it up
            possible_rank = LookupTables.unique5[q]
            if possible_rank != 0:
                return possible_rank
            else:
                # We need a different lookup table with different keys
                # Compute the unique product of primes, because we have a pair
                # or trips, etc. Use the product to look up the rank.
                q = reduce(mul, map(lambda card: card & 0xFF, bh))
                # Here, use dict instead of sparse array (basically hashing)
                # I didn't bother using "perfect hash", the python hashing
                # shouldn't be terrible
                return LookupTables.pairs.get(q)

    evaluate_preflop_hand = staticmethod(evaluate_preflop_hand)        
    evaluate_hand = staticmethod(evaluate_hand)
    card_to_binary = staticmethod(card_to_binary)
    card_to_binary_lookup = staticmethod(card_to_binary_lookup)
    evaluate_rank = staticmethod(evaluate_rank)