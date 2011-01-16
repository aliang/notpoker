import sys
sys.path.append("../")
from pokerbots.engine.game import Card
from pokerbots.player.hand_evaluator import HandEvaluator
from pokerbots.player.lookup_tables import LookupTables
from itertools import combinations, permutations
from collections import defaultdict
from operator import add, mul, __or__

# Use three different suits, since we assume not a flush
# Otherwise the rank will be too high

# chunk things so we can print in lines instead of one big line
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

# TODO: Verify we get the right results...
def write_flush_rank_bits_to_rank():
    result = {}
    for combination in combinations(xrange(13), 6):
        # Should have 13 choose 6 = 1716
        combo = list(combination)
        bits = reduce(__or__, map(lambda rank: 1 << rank, combination))
        cards = [Card(combo[0] + 2, 1),
            Card(combo[1] + 2, 1),
            Card(combo[2] + 2, 1),
            Card(combo[3] + 2, 1),
            Card(combo[4] + 2, 1),
            Card(combo[5] + 2, 1)]
        hand_combinations = combinations(cards, 5)
        result[bits] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    for combination in combinations(xrange(13), 5):
        # Should have 13 choose 5 = 1287
        combo = list(combination)
        bits = reduce(__or__, map(lambda rank: 1 << rank, combination))
        cards = [Card(combo[0] + 2, 1),
            Card(combo[1] + 2, 1),
            Card(combo[2] + 2, 1),
            Card(combo[3] + 2, 1),
            Card(combo[4] + 2, 1)]
        result[bits] = HandEvaluator.Five.evaluate_rank(cards)
    
    assert len(result) == 1716 + 1287
    fh = open("six.flush_rank_bits_to_rank.py", "w")
    fh.write("flush_rank_bits_to_rank = {\n")
    for key_group in chunker(result.keys(), 4):
        if len(key_group) == 4:
            fh.write("%s: %s, %s: %s, %s: %s, %s: %s,\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]],
                key_group[2], result[key_group[2]],
                key_group[3], result[key_group[3]]))
        else: # last group has 3
            fh.write("%s: %s, %s: %s, %s: %s\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]],
                key_group[2], result[key_group[2]]))
    fh.write("}")
    fh.close()

def write_prime_products_to_rank(): # 4-0, 2-1, 0-2
    """
    Write a table mapping products of 6 ranks' corresponding prime
    numbers to hand rank. Only do it for hands in certain combinations,
    though, or the table gets really big.
    """
    result = {}
    
    # Choose four ranks, frequency (1,1,1,3)    
    for combination in combinations(xrange(13), 4):
        # Choose each one to appear three times
        # Should be 4 * 13 choose 4 = 2860
        combo = list(combination)
        for i in xrange(4):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:4]
            prime_for_rank = LookupTables.primes[rank]
            
            # first get the product we need
            product = prime_for_rank * prime_for_rank * prime_for_rank * \
                reduce(mul,
                    map(lambda rank: LookupTables.primes[rank], other_ranks))
            
            # now generate the hand we need
            hand = [Card(rank + 2,1), Card(rank + 2,2), Card(rank + 2,3)]
            hand = hand + map(lambda rank: Card(rank + 2,4), other_ranks)
            hand_combinations = combinations(hand, 5)
            # now map the product to the 5-card hand rank
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # Choose three cards, frequencies (1,1,4) and (1,3,2)
    for combination in combinations(xrange(13), 3):
        combo = list(combination)
        # Choose each one to appear four times for (1,1,4)
        # Should be 3 * 13 choose 3 = 858
        for i in xrange(3):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:3]
            prime_for_rank = LookupTables.primes[rank]
            
            product = prime_for_rank * prime_for_rank * \
                prime_for_rank * prime_for_rank * \
                reduce(mul,
                    map(lambda rank: LookupTables.primes[rank], other_ranks))
            
            hand = [Card(rank + 2,1),Card(rank + 2,2),
                Card(rank + 2,3),Card(rank + 2,4)]
            hand = hand + map(lambda rank: Card(rank + 2,4), other_ranks)
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
        
        # Now for each combination, permute so that we can do (1,3,2)
        # Should be 6 * 13 choose 3 = 1716
        for permute in permutations(combo):
            # permute contains the ranks in each order
            primes = map(lambda rank: LookupTables.primes[rank], permute)
            product = primes[0] * primes[1] * primes[1] * primes[1] * primes[2] * primes[2]
            hand = [Card(permute[0] + 2, 1),
                Card(permute[1] + 2, 2),
                Card(permute[1] + 2, 3),
                Card(permute[1] + 2, 4),
                Card(permute[2] + 2, 1),
                Card(permute[2] + 2, 2)]
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))

    # Choose two ranks, frequencies (2,4)
    for combination in combinations(xrange(13), 2):
        combo = list(combination)
        # Each needs to be the two once
        # Should have 2 * 13 choose 2 = 156
        for permute in permutations(combo):
            # permute contains the ranks in each order
            primes = map(lambda rank: LookupTables.primes[rank], permute)
            product = primes[0] * primes[0] * primes[1] * primes[1] * primes[1] * primes[1]
            hand = [Card(permute[0] + 2, 1),
                Card(permute[0] + 2, 2),
                Card(permute[1] + 2, 3),
                Card(permute[1] + 2, 4),
                Card(permute[1] + 2, 1),
                Card(permute[1] + 2, 2)]
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # at the end, we should have 2860 + 858 + 1716 + 156 keys in the table
    assert len(result) == (2860 + 858 + 1716 + 156)
    fh = open("six.prime_products_to_rank.py", "w")
    fh.write("prime_products_to_rank = {\n")
    for key_group in chunker(result.keys(), 4):
        if len(key_group) == 4:
            fh.write("%s: %s, %s: %s, %s: %s, %s: %s,\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]],
                key_group[2], result[key_group[2]],
                key_group[3], result[key_group[3]]))
        else: # last group has 2
            fh.write("%s: %s, %s: %s\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]]))
    fh.write("}")
    fh.close()

def write_odd_xors_to_rank(): # 6-0, 2-0
    result = {}
    
    for combination in combinations(xrange(13), 6):
        # in the case where six different bits are set, you
        # can substitute or
        # Should have 13 choose 6 = 1716
        odd_xor = reduce(__or__, map(lambda rank: 1 << rank, combination))
        hand = [Card(combination[0] + 2,1),
            Card(combination[1] + 2,2),
            Card(combination[2] + 2,3),
            Card(combination[3] + 2,4),
            Card(combination[4] + 2,1),
            Card(combination[5] + 2,2)]
        hand_combinations = combinations(hand, 5)
        result[odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    for combination in combinations(xrange(13), 2):
        # convert to rank number with 2 bits on
        # by only choosing two numbers, we can use or instead of xor
        # Should have 13 choose 2 = 78
        odd_xor = reduce(__or__, map(lambda rank: 1 << rank, combination))
        hand = [Card(combination[0] + 2,1),
            Card(combination[0] + 2,2),
            Card(combination[0] + 2,3),
            Card(combination[1] + 2,4),
            Card(combination[1] + 2,1),
            Card(combination[1] + 2,2)]
        hand_combinations = combinations(hand, 5)
        result[odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    assert len(result) == 1716 + 78
    fh = open("six.odd_xors_to_rank.py", "w")
    fh.write("odd_xors_to_rank = {\n")
    for key_group in chunker(result.keys(), 4):
        if len(key_group) == 4:
            fh.write("%s: %s, %s: %s, %s: %s, %s: %s,\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]],
                key_group[2], result[key_group[2]],
                key_group[3], result[key_group[3]]))
        else: # last group has 2
            fh.write("%s: %s, %s: %s\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]]))
    fh.write("}")
    fh.close()

def write_even_xors_to_rank(): # 0-3
    result = {}
    for combination in combinations(xrange(13), 3):
        # you can just use or again, since they're all the same
        # Should have 13 choose 3 = 286
        even_xor = reduce(__or__, map(lambda rank: 1 << rank, combination))
        hand = [Card(combination[0] + 2,1),
            Card(combination[0] + 2,2),
            Card(combination[1] + 2,3),
            Card(combination[1] + 2,4),
            Card(combination[2] + 2,1),
            Card(combination[2] + 2,2)]
        hand_combinations = combinations(hand, 5)
        result[even_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    assert len(result) == 286
    fh = open("six.even_xors_to_rank.py", "w")
    fh.write("even_xors_to_rank = {\n")
    for key_group in chunker(result.keys(), 4):
        if len(key_group) == 4:
            fh.write("%s: %s, %s: %s, %s: %s, %s: %s,\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]],
                key_group[2], result[key_group[2]],
                key_group[3], result[key_group[3]]))
        else: # last group has 2
            fh.write("%s: %s, %s: %s\n" % (
                key_group[0], result[key_group[0]],
                key_group[1], result[key_group[1]]))
    fh.write("}")
    fh.close()

def write_even_xors_to_odd_xors_to_rank(): # 4-1, 2-2
    result = defaultdict(dict)
    # choose five ranks, frequencies (1,1,1,1,2)
    for combination in combinations(xrange(13), 5):
        # Choose each one to appear twice
        # Should be 5 * 13 choose 5 = 6435
        combo = list(combination)
        for i in xrange(5):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:5]
            
            even_xor = 1 << rank
            odd_xor = reduce(__or__, map(lambda rank: 1 << rank, other_ranks))
            
            # now generate the hand we need
            hand = [Card(rank + 2,1), Card(rank + 2,2)]
            hand = hand + map(lambda rank: Card(rank + 2,3), other_ranks)
            hand_combinations = combinations(hand, 5)
            # now map the product to the 5-card hand rank
            result[even_xor][odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # choose four ranks, frequencies (1,1,2,2)
    for combination in combinations(xrange(13), 4):
        # Now choose every possible pair from those four to appear twice
        # Should have (4 choose 2) * (13 choose 4) = 6 * 715 = 4290
        combo = list(combination)
        for pair_ranks in combinations(combo, 2):
            one_ranks = filter(lambda rank: rank not in pair_ranks, combo)
            
            even_xor = reduce(__or__, map(lambda rank: 1 << rank, pair_ranks))
            odd_xor = reduce(__or__, map(lambda rank: 1 << rank, one_ranks))
            
            hand = [Card(pair_ranks[0] + 2,1),
                Card(pair_ranks[0] + 2,2),
                Card(pair_ranks[1] + 2,3),
                Card(pair_ranks[1] + 2,4),
                Card(one_ranks[0] + 2,1),
                Card(one_ranks[1] + 2,2)]
            hand_combinations = combinations(hand, 5)
            result[even_xor][odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # this assertion is more complex
    # First, count the even_xor keys
    assert len(result) == 13 + 78
    # Then count the leaves
    assert reduce(add, map(lambda even_xor: len(result[even_xor]), result)) == 6435 + 4290
    fh = open("six.even_xors_to_odd_xors_rank.py", "w")
    fh.write("even_xors_to_odd_xors_to_rank = {\n")
    for even_xor in result.keys():
        fh.write("%s: { " % (even_xor,))
        fh.write(", ".join(map(lambda odd_xor: "%s: %s" % (odd_xor, result[even_xor][odd_xor]),
            result[even_xor].keys())))
        fh.write(" },\n")
    fh.write("}")
    fh.close()

write_prime_products_to_rank()