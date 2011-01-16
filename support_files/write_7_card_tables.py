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

def write_prime_products_to_flush():
    result = {}
    primes = (2,3,5,7,)
    # python 2.6 doesn't have combinations with replacement, which would make
    # this super easy.
    for i in primes:
        for j in primes:
            for k in primes:
                product = i * i * i * i * i * j * k
                result[product] = i
    fh = open("seven.prime_products_to_flush.py", "w")
    fh.write("prime_products_to_flush = {\n")
    fh.write(",\n".join(map(
        lambda chunk: ", ".join(map(
            lambda k: "%s: %s" % (k, result[k]),
            chunk)),
        chunker(sorted(result.keys()), 8))))
    fh.write("}")
    fh.close()

# TODO: Verify we get the right results...
def write_flush_rank_bits_to_rank():
    result = {}
    for i in xrange(5,8): # 5,6,7 ranks of same suit
        # Should have 13 choose 7 plus 13 choose 6 plus 13 choose 5 
        # which is 1716 + 1716 + 1287 = 4719
        for combination in combinations(xrange(13), i):
            combo = list(combination)
            bits = reduce(__or__, map(lambda rank: 1 << rank, combination))
            cards = map(lambda rank: Card(rank + 2, 1), combination)
            hand_combinations = combinations(cards, 5)
            result[bits] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    assert len(result) == 1716 + 1716 + 1287
    fh = open("seven.flush_rank_bits_to_rank.py", "w")
    fh.write("flush_rank_bits_to_rank = {\n")
    fh.write(",\n".join(map(
        lambda chunk: ", ".join(map(
            lambda k: "%s: %s" % (k, result[k]),
            chunk)),
        chunker(result.keys(), 4))))
    fh.write("}")
    fh.close()

def write_odd_xors_to_rank(): # 7-0
    result = {}

    for combination in combinations(xrange(13), 7):
        # All bits are different, so you can just use or
        # Should have 13 choose 7 = 1716
        odd_xor = reduce(__or__, map(lambda rank: 1 << rank, combination))
        hand = [Card(combination[0] + 2,1),
            Card(combination[1] + 2,2),
            Card(combination[2] + 2,3),
            Card(combination[3] + 2,4),
            Card(combination[4] + 2,1),
            Card(combination[5] + 2,2),
            Card(combination[6] + 2,3)]
        hand_combinations = combinations(hand, 5)
        result[odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    assert len(result) == 1716
    fh = open("seven.odd_xors_to_rank.py", "w")
    fh.write("odd_xors_to_rank = {\n")
    fh.write(",\n".join(map(
        lambda chunk: ", ".join(map(
            lambda k: "%s: %s" % (k, result[k]),
            chunk)),
        chunker(result.keys(), 4))))
    fh.write("}")
    fh.close()

def write_prime_products_to_rank(): # 5-0, 3-0, 3-1, 1-2
    """
    Write a table mapping products of 6 ranks' corresponding prime
    numbers to hand rank. Only do it for hands in certain combinations,
    though, or the table gets really big.
    """
    result = {}
    
    # Choose five ranks, frequency (1,1,1,1,3)
    for combination in combinations(xrange(13), 5):
        # Choose each one to appear three times
        # Should be 5 * 13 choose 5 = 6435
        combo = list(combination)
        for i in xrange(5):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:5]
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
    
    # Choose three cards, frequencies (1,3,3), (1,2,4), or (3,2,2)
    for combination in combinations(xrange(13), 3):
        combo = list(combination)
        # Choose each one to appear once (1,3,3)
        # Same one can be the 3 in (3,2,2)
        # Should be 2 * 3 * 13 choose 3 = 1716
        for i in xrange(3):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:3]
            prime_for_rank = LookupTables.primes[rank]
            
            # (1,3,3)
            product = prime_for_rank * reduce(mul,
                map(lambda rank: LookupTables.primes[rank] * LookupTables.primes[rank] * LookupTables.primes[rank],
                    other_ranks))
            
            hand = [Card(rank + 2,1),
                Card(other_ranks[0] + 2,2),
                Card(other_ranks[0] + 2,3),
                Card(other_ranks[0] + 2,4),
                Card(other_ranks[1] + 2,1),
                Card(other_ranks[1] + 2,2),
                Card(other_ranks[1] + 2,3)]
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
            
            # (3,2,2)
            product = prime_for_rank * prime_for_rank * prime_for_rank * reduce(mul,
                map(lambda rank: LookupTables.primes[rank] * LookupTables.primes[rank],
                    other_ranks))
            hand = [Card(rank + 2,1),
                Card(rank + 2,2),
                Card(rank + 2,3),
                Card(other_ranks[0] + 2,1),
                Card(other_ranks[0] + 2,2),
                Card(other_ranks[1] + 2,3),
                Card(other_ranks[1] + 2,4)]
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
        
        # Permute each combination (1,2,4)
        # Should be 6 * 13 choose 3 = 1716
        for permute in permutations(combination):
            one = permute[0]
            two = permute[1]
            four = permute[2]
            
            product = LookupTables.primes[one] *\
                LookupTables.primes[two] * LookupTables.primes[two] *\
                LookupTables.primes[four] * LookupTables.primes[four] *\
                LookupTables.primes[four] * LookupTables.primes[four]
            hand = [Card(one + 2,1),
                Card(two + 2,2),
                Card(two + 2,3),
                Card(four + 2,1),
                Card(four + 2,2),
                Card(four + 2,3),
                Card(four + 2,4)]
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
        
    # Choose four ranks, frequencies (1,1,1,4) and (1,1,3,2)
    for combination in combinations(xrange(13), 4):
        combo = list(combination)
        # Choose one to be the 4
        # This one is also the 3
        for i in xrange(4):
            # Deal with (1,1,1,4)
            # Should have 4 * 13 choose 4 = 2860
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:4]
            prime_for_rank = LookupTables.primes[rank]
            
            product = prime_for_rank * prime_for_rank *\
                prime_for_rank * prime_for_rank *\
                reduce(mul, map(lambda rank: LookupTables.primes[rank], other_ranks))
            hand = [Card(rank + 2,1),
                Card(rank + 2,2),
                Card(rank + 2,3),
                Card(rank + 2,4)]
            hand = hand + map(lambda rank: Card(rank + 2, 1), other_ranks)
            hand_combinations = combinations(hand, 5)
            result[product] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
            
            # Use the 4 as the 3 now
            # Now pick another to be the 2 to do (1,1,3,2)
            # Should have 4 * 3 * 13 choose 4 = 8580
            three = rank
            for j in xrange(3):
                two = other_ranks[j]
                ones = other_ranks[0:j] + other_ranks[j+1:3]
                
                product = LookupTables.primes[three] * LookupTables.primes[three] * LookupTables.primes[three] *\
                    LookupTables.primes[two] * LookupTables.primes[two] *\
                    LookupTables.primes[ones[0]] * LookupTables.primes[ones[1]]
                hand = [Card(three + 2, 1),
                    Card(three + 2, 2),
                    Card(three + 2, 3),
                    Card(two + 2, 1),
                    Card(two + 2, 2),
                    Card(ones[0] + 2, 1),
                    Card(ones[1] + 2, 2)]
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
    assert len(result) == (6435 + 1716 + 1716 + 2860 + 8580 + 156)
    fh = open("seven.prime_products_to_rank.py", "w")
    fh.write("prime_products_to_rank = {\n")
    fh.write(",\n".join(map(
        lambda chunk: ", ".join(map(
            lambda k: "%s: %s" % (k, result[k]),
            chunk)),
        chunker(result.keys(), 4))))
    fh.write("}")
    fh.close()

def write_even_xors_to_odd_xors_to_rank(): # 5-1, 3-2, 1-3, 1-1
    result = defaultdict(dict)
    # choose six ranks, frequencies (1,1,1,1,1,2))
    for combination in combinations(xrange(13), 6):
        # Choose each one to appear twice
        # Should be 6 * 13 choose 6 = 10296
        combo = list(combination)
        for i in xrange(6):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:6]
            
            even_xor = 1 << rank
            odd_xor = reduce(__or__, map(lambda rank: 1 << rank, other_ranks))
            
            # now generate the hand we need
            hand = [Card(rank + 2,1), Card(rank + 2,2),
                Card(other_ranks[0] + 2, 3),
                Card(other_ranks[1] + 2, 4),
                Card(other_ranks[2] + 2, 1),
                Card(other_ranks[3] + 2, 2),
                Card(other_ranks[4] + 2, 3),
            ]
            hand_combinations = combinations(hand, 5)
            # now map the product to the 5-card hand rank
            result[even_xor][odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # choose five ranks, frequencies (1,1,1,2,2)
    for combination in combinations(xrange(13), 5):
        # Now choose every possible pair from those five to appear twice
        # Should have (5 choose 2) * (13 choose 5) = 12870
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
                Card(one_ranks[1] + 2,2),
                Card(one_ranks[2] + 2,3)]
            hand_combinations = combinations(hand, 5)
            result[even_xor][odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # choose four ranks, frequencies (1,2,2,2)
    for combination in combinations(xrange(13), 4):
        # Now choose every possible rank to be the 1
        # Should have 4 * 13 choose 4 = 2860
        combo = list(combination)
        for i in xrange(4):
            rank = combo[i]
            other_ranks = combo[0:i] + combo[i+1:4]
            
            even_xor = reduce(__or__, map(lambda rank: 1 << rank, other_ranks))
            odd_xor = 1 << rank
            
            # now generate the hand we need
            hand = [Card(rank + 2,1),
                Card(other_ranks[0] + 2, 2),
                Card(other_ranks[0] + 2, 3),
                Card(other_ranks[1] + 2, 4),
                Card(other_ranks[1] + 2, 1),
                Card(other_ranks[2] + 2, 2),
                Card(other_ranks[2] + 2, 3),
            ]
            hand_combinations = combinations(hand, 5)
            # now map the product to the 5-card hand rank
            result[even_xor][odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # choose two ranks, frequencies (3,4)
    for combination in combinations(xrange(13), 2):
        # Both can be the 3
        # Should have 2 * 13 choose 2 = 156
        combo = list(combination)
        for i in xrange(2):
            three = combo[i]
            four = combo[1 - i]
            
            even_xor = 1 << four
            odd_xor = 1 << three
            
            hand = [Card(three + 2, 1),
                Card(three + 2, 2),
                Card(three + 2, 3),
                Card(four + 2, 1),
                Card(four + 2, 2),
                Card(four + 2, 3),
                Card(four + 2, 4)]
            hand_combinations = combinations(hand, 5)
            result[even_xor][odd_xor] = min(map(HandEvaluator.Five.evaluate_rank, hand_combinations))
    
    # this assertion is more complex
    # First, count the even_xor keys
    assert len(result) == 13 + 78 + 286
    # Then count the leaves
    assert reduce(add, map(lambda even_xor: len(result[even_xor]), result)) == 10296 + 12870 + 2860 + 156
    fh = open("seven.even_xors_to_odd_xors_rank.py", "w")
    fh.write("even_xors_to_odd_xors_to_rank = {\n")
    for even_xor in result.keys():
        fh.write("%s: { " % (even_xor,))
        fh.write(",\n".join(map(
            lambda chunk: ", ".join(map(
                lambda odd_xor: "%s: %s" % (odd_xor, result[even_xor][odd_xor]),
                chunk)),
            chunker(result[even_xor].keys(), 4))))
        fh.write(" },\n")
    fh.write("}")
    fh.close()

# write_prime_products_to_flush()
# write_flush_rank_bits_to_rank()
# write_odd_xors_to_rank()
# write_prime_products_to_rank()
write_even_xors_to_odd_xors_to_rank()