from lookup_tables import LookupTables
from popcount import PopCount
from itertools import combinations
from operator import mul, __or__, __and__, __xor__

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

class HandEvaluator:
    class Five:
        def card_to_binary(card):
            """
            Convert the pokerbots.engine.game.Card representation to a binary
            representation for use in 5-card hand evaluation
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
            return LookupTables.Five.card_to_binary[card.rank][card.suit]

        # TODO: Return a class of hand too? Would be useful to see if we can make
        # a draw or something.
        def evaluate_rank(hand):
            """
            Return the rank of this 5-card hand amongst all 5-card hands.
            """
            # This implementation uses the binary representation from
            # card_to_binary
            card_to_binary = HandEvaluator.Five.card_to_binary_lookup

            # bh stands for binary hand
            bh = map(card_to_binary, hand)
            has_flush = reduce(__and__, bh, 0xF000)
            # This is a unique number based on the ranks if your cards,
            # assuming your cards are all different
            q = reduce(__or__, bh) >> 16
            if has_flush:
                # Look up the rank of this flush
                return LookupTables.Five.flushes[q]
            else:
                # The q still works as a key if you have 5 unique cards,
                # so see if we can look it up
                possible_rank = LookupTables.Five.unique5[q]
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
                    return LookupTables.Five.pairs.get(q)

        card_to_binary = staticmethod(card_to_binary)
        card_to_binary_lookup = staticmethod(card_to_binary_lookup)
        evaluate_rank = staticmethod(evaluate_rank)
    
    class Six:
        def card_to_binary(card):
            """
            Convert the pokerbots.engine.game.Card representation to a binary
            representation for use in 6-card hand evaluation
            """
            # This a variant on Cactus Kev's algorithm. We need to replace
            # the 4-bit representation of suit with a prime number representation
            # so we can look up whether something is a flush by prime product
        
            # First we need to generate the following representation
            # Bits marked x are not used.
            # xxxbbbbb bbbbbbbb qqqqrrrr xxpppppp
        
            # b is one bit flipped for A-2
            # q is 2, 3, 5, or 7 for spades, hearts, clubs, diamonds
            # r is just the numerical rank in binary, with deuce = 0
            # p is the prime from LookupTable.primes corresponding to the rank,
            # in binary
            # Then shift appropriately to fit the template above
            b_mask = 1 << (14 + card.rank)
            q_mask = LookupTables.primes[card.suit - 1] << 12
            r_mask = (card.rank - 2) << 8
            p_mask = LookupTables.primes[card.rank - 2]
            # OR them together to get the final result
            return b_mask | q_mask | r_mask | p_mask
        
        def card_to_binary_lookup(card):
            return LookupTables.Six.card_to_binary[card.rank][card.suit]
    
        def evaluate_rank(hand):
            """
            Return the rank amongst all possible 5-card hands of any kind
            using the best 5-card hand from the given 6-card hand.
            """
            # bh stands for binary hand, map to that representation
            card_to_binary = HandEvaluator.Six.card_to_binary
            bh = map(card_to_binary, hand)
        
            # We can determine if it's a flush using a lookup table.
            # Basically use prime number trick but map to bool instead of rank
            # Once you have a flush, there is no other higher hand you can make
            # except straight flush, so just need to determine the highest flush
            flush_prime = reduce(mul, map(lambda card: (card >> 12) & 0xF, bh))
            flush_suit = False
            if flush_prime in LookupTables.Six.prime_products_to_flush:
                flush_suit = LookupTables.Six.prime_products_to_flush[flush_prime]
        
            # Now use ranks to determine hand via lookup
            odd_xor = reduce(__xor__, bh) >> 16
            even_xor = (reduce(__or__, bh) >> 16) ^ odd_xor
            # If you have a flush, use odd_xor to find the rank
            # That value will have either 4 or 5 bits
            if flush_suit:
                if even_xor == 0:
                    # just filter out the card(s) not in the right suit
                    # TODO: There might be a faster way?
                    bits = reduce(__or__, map(
                        lambda card: (card >> 16),
                        filter(
                            lambda card: (card >> 12) & 0xF == flush_suit, bh)))
                    return LookupTables.Six.flush_rank_bits_to_rank[bits]
                else:
                    # you have a pair, one card in the flush suit,
                    # so just use the ranks you have by or'ing the two
                    return LookupTables.Six.flush_rank_bits_to_rank[odd_xor | even_xor]
        
            # Otherwise, get ready for a wild ride:
        
            # Can determine this by using 2 XORs to reduce the size of the
            # lookup. You have an even number of cards, so any odd_xor with
            # an odd number of bits set is not possible.
            # Possibilities are odd-even:
            # 6-0 => High card or straight (1,1,1,1,1,1)
            #   Look up by odd_xor
            # 4-1 => Pair (1,1,1,1,2)
            #   Look up by even_xor (which pair) then odd_xor (which set of kickers)
            # 4-0 => Trips (1,1,1,3)
            #   Don't know which one is the triple, use prime product of ranks
            # 2-2 => Two pair (1,1,2,2)
            #   Look up by odd_xor then even_xor (or vice-versa)
            # 2-1 => Four of a kind (1,1,4) or full house (1,3,2)
            #   Look up by prime product
            # 2-0 => Full house using 2 trips (3,3)
            #   Look up by odd_xor
            # 0-3 => Three pairs (2,2,2)
            #   Look up by even_xor
            # 0-2 => Four of a kind with pair (2,4)
            #   Look up by prime product
        
            # Any time you can't disambiguate 2/4 or 1/3, use primes.
            # We also assume you can count bits or determine a power of two.
            # (see PopCount class.)
            
            if even_xor == 0: # x-0
                odd_popcount = PopCount.popcount(odd_xor)
                if odd_popcount == 4: # 4-0
                    prime_product = reduce(mul, map(lambda card: card & 0xFF, bh))
                    return LookupTables.Six.prime_products_to_rank[prime_product]
                else: # 6-0, 2-0
                    return LookupTables.Six.odd_xors_to_rank[odd_xor]
            elif odd_xor == 0: # 0-x
                even_popcount = PopCount.popcount(even_xor)
                if even_popcount == 2: # 0-2
                    prime_product = reduce(mul, map(lambda card: card & 0xFF, bh))
                    return LookupTables.Six.prime_products_to_rank[prime_product]
                else: # 0-3
                    return LookupTables.Six.even_xors_to_rank[even_xor]
            else: # odd_popcount is 4 or 2
                odd_popcount = PopCount.popcount(odd_xor)
                if odd_popcount == 4: # 4-1
                    return LookupTables.Six.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
                else: # 2-x
                    even_popcount = PopCount.popcount(even_xor)
                    if even_popcount == 2: # 2-2
                        return LookupTables.Six.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
                    else: # 2-1
                        prime_product = reduce(mul, map(lambda card: card & 0xFF, bh))
                        return LookupTables.Six.prime_products_to_rank[prime_product]

        card_to_binary = staticmethod(card_to_binary)
        card_to_binary_lookup = staticmethod(card_to_binary_lookup)
        evaluate_rank = staticmethod(evaluate_rank)
    
    class Seven:
        def card_to_binary(card):
            """
            Convert the pokerbots.engine.game.Card representation to a binary
            representation for use in 7-card hand evaluation
            """
            return None
        
        def card_to_binary_lookup(card):
            return None
        
        def evaluate_rank(hand):
            """
            Return the rank amongst all possible 5-card hands of any kind
            using the best 5-card hand from the given 6-card hand.
            """
            # bh stands for binary hand, map to that representation
            card_to_binary = HandEvaluator.Seven.card_to_binary
            bh = map(card_to_binary, hand)
        
            # Use a lookup table to determine if it's a flush as with 6 cards
            flush_prime = reduce(mul, map(lambda card: (card >> 12) & 0xF, bh))
            flush_suit = False
            if flush_prime in LookupTables.Seven.prime_products_to_flush:
                flush_suit = LookupTables.Seven.prime_products_to_flush[flush_prime]
        
            # Now use ranks to determine hand via lookup
            odd_xor = reduce(__xor__, bh) >> 16
            even_xor = (reduce(__or__, bh) >> 16) ^ odd_xor
            # If you have a flush, use odd_xor to find the rank
            # That value will have either 3, 5 or 7 bits
            if flush_suit:
                if even_xor == 0:
                    # just filter out the card(s) not in the right suit
                    # TODO: There might be a faster way?
                    bits = reduce(__or__, map(
                        lambda card: (card >> 16),
                        filter(
                            lambda card: (card >> 12) & 0xF == flush_suit, bh)))
                    return LookupTables.Six.flush_rank_bits_to_rank[bits]
                else:
                    # you have a pair, one card in the flush suit,
                    # so just use the ranks you have by or'ing the two
                    return LookupTables.Six.flush_rank_bits_to_rank[odd_xor | even_xor]
            
            # Odd-even XOR again, see Six.evaluate_rank for details
            # 7 is odd, so you have to have an odd number of bits in odd_xor
            #x 7-0 => (1,1,1,1,1,1,1)
            # 5-1 => (1,1,1,1,1,2)
            #x 5-0 => (1,1,1,1,3)
            # 3-2 => (1,1,1,2,2)
            # 3-1 => (1,1,1,4) or (1,1,3,2)
            #x 3-0 => (1,3,3)
            # 1-3 => (1,2,2,2)
            # 1-2 => (1,2,4) or (3,2,2)
            
            if even_xor == 0: # x-0                
                pass
            else:
                pass
        card_to_binary = staticmethod(card_to_binary)
        card_to_binary_lookup = staticmethod(card_to_binary_lookup)
        evaluate_rank = staticmethod(evaluate_rank)

    # These are the main functions, we have to define them afterwards
    def evaluate_hand(cards):
        """
        Return the rank and percentile of the best 5 card hand made from these
        cards, against an equivalent number of cards.
        Rank is given as a dict with:
            rank: rank within the 7462 equivalence classes,
            percentile: the percentile of hands you beat based on this rank
        """

        # Default values in case we screw up
        rank = 7463
        percentile = 0.0
        if len(cards) == 5:
            rank = HandEvaluator.Five.evaluate_rank(cards)
            # TODO: The space is different because only two cards vary.
            # The percentiles we look up are against any 5, 6, or 7 cards,
            # not against any 2. So we need to update this.
            percentile = LookupTables.Five.rank_to_percentile_5[rank - 1]
        elif len(cards) == 6:
            # evaluate all hands, choose the best one.
            # warning, don't pass too many cards here...
            try:
                rank = HandEvaluator.Six.evaluate_rank(cards)
            except:
                possible_hands = combinations(cards, 5)
                rank = min(map(HandEvaluator.Five.evaluate_rank, possible_hands))
            percentile = LookupTables.Five.rank_to_percentile_6[rank - 1]
        elif len(cards) == 7:
            try:
                rank = HandEvaluator.Seven.evaluate_rank(cards)
            except:
                possible_hands = combinations(cards, 5)
                rank = min(map(HandEvaluator.Five.evaluate_rank, possible_hands))
            percentile = LookupTables.Five.rank_to_percentile_7[rank - 1]
        return {
            'rank': rank,
            'percentile': percentile
        }

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
            preflop_order = LookupTables.Two.preflop_order_matrix[sorted_rank[1] - 2][sorted_rank[0] - 2]
        else:
            preflop_order = LookupTables.Two.preflop_order_matrix[sorted_rank[0] - 2][sorted_rank[1] - 2]

        # this is fraction of hands you beat
        preflop_percentile = 1 - sum(LookupTables.Two.preflop_count_matrix[0:preflop_order - 1]) / \
            LookupTables.Two.preflop_count_sum

        return {
            'rank': preflop_order,
            'percentile': preflop_percentile
        }
    evaluate_preflop_hand = staticmethod(evaluate_preflop_hand)
    evaluate_hand = staticmethod(evaluate_hand)