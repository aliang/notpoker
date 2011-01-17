import sys
sys.path.append("../")
from pokerbots.player.lookup_tables import LookupTables
from itertools import combinations

def write_preflop_percentiles():
    """
    Return the fraction of other hands you beat before the flop
    (assuming opponent has any two cards).
    """
    suited_result = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # not used
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 2
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 5
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 6
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 7
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 8
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 9
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 10
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # J
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Q
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # K
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # A
    ]
    unsuited_result = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # not used
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 2
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 5
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 6
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 7
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 8
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 9
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 10
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # J
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Q
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # K
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # A
    ]
    hands = combinations(LookupTables.deck, 2)
    # This could be faster, but it doesn't run very much so whatever
    for hand in hands:
        sorted_rank = sorted([hand[0].rank, hand[1].rank])
        if hand[0].suit == hand[1].suit:
            preflop_order = LookupTables.Two.preflop_order_matrix[sorted_rank[1] - 2][sorted_rank[0] - 2]
        else:
            preflop_order = LookupTables.Two.preflop_order_matrix[sorted_rank[0] - 2][sorted_rank[1] - 2]

        # this is fraction of hands you beat
        preflop_percentile = 1 - sum(LookupTables.Two.preflop_count_matrix[0:preflop_order - 1]) / \
            LookupTables.Two.preflop_count_sum

        if hand[0].suit == hand[1].suit:
            suited_result[hand[0].rank][hand[1].rank] = preflop_percentile
        else:
            unsuited_result[hand[0].rank][hand[1].rank] = preflop_percentile
    
    print "suited_ranks_to_percentile = ["
    for sublist in suited_result:
        print sublist
    print "]"
    
    print "unsuited_ranks_to_percentile = ["
    for sublist in unsuited_result:
        print sublist
    print "]"
    
write_preflop_percentiles()