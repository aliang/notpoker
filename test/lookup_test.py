# This is just a file to test the lookup bot
# primes = [2,3,5,7,11,13,17,19,23,29,31,37,41]
import sys
sys.path.append("../")
from pokerbots.engine.game import Card
from pokerbots.player.hand_evaluator import HandEvaluator
from itertools import combinations

# 2 card hands
hands_2 = {
    "7-2": [Card(2,1), Card(7,2)],
    "7-2 suited": [Card(2,1), Card(7,1)],
    "9-8 suited": [Card(8,1), Card(9,1)],
    "6-6": [Card(6,1), Card(6,2)],
    "10-10": [Card(10,2), Card(10,3)],
    "A-K": [Card(14,3), Card(13,3)],
    "big slick": [Card(14,3), Card(13,3)],
    "rockets": [Card(14,3), Card(14,2)]
}

# 5 card hands
hands_5 = {
    "straight flush": [Card(14,1),Card(13,1),Card(12,1),Card(11,1),Card(10,1)],
    "quads": [Card(7,1),Card(7,2),Card(7,3),Card(7,4),Card(9,1)],
    "full house": [Card(12,1), Card(12,2), Card(12,3), Card(6,4), Card(6,3)],
    # 5-card flush with 6 cards
    "flush": [Card(7,1),Card(13,1),Card(12,1),Card(11,1),Card(9,1)],
    # 6-card flush with 6 cards
    "flush-2": [Card(7,3),Card(14,3),Card(12,3),Card(11,3),Card(9,3)],
    # 5-card flush with pair with 6 cards
    "flush-3": [Card(2,3),Card(4,3),Card(6,3),Card(8,3),Card(10,2)],
    "straight": [Card(3,2), Card(4,2), Card(5,3), Card(6,4), Card(7,1)],
    "trips": [Card(12,1), Card(12,2), Card(12,3), Card(6,4), Card(9,3)],
    "two pair": [Card(12,1), Card(12,2), Card(9,3), Card(6,4), Card(6,3)],
    "pair": [Card(12,1), Card(12,2), Card(14,3), Card(8,4), Card(6,3)],
    "high card": [Card(8,4), Card(3,1), Card(14,1), Card(13,2), Card(9,3),]
}
# 6/7 card hands--they should evaluate to the same 5-card hands though
# (except high-card/kicker stuff)
hands_6 = {}
for k in hands_5.keys():
    hands_6[k] = hands_5[k] + [Card(10,3)]
hands_6_more = {}
hands_7 = {}
for k in hands_6.keys():
    hands_7[k] = hands_6[k] + [Card(2,4)]

print "----Testing 2-card hands----"
for k in sorted(hands_2.keys()):
    cards = hands_2[k]
    print "Percentile of %s is %s (%s expected)" % (k,
        HandEvaluator.evaluate_hand(cards),
        HandEvaluator.evaluate_preflop_hand(cards)
    )
print "----Testing 5-card hands----"
for k in sorted(hands_5.keys()):
    cards = hands_5[k]
    print "Rank of %s is %s" % (k, HandEvaluator.Five.evaluate_rank(cards))
    print "Percentile of %s is %s" % (k, HandEvaluator.evaluate_hand(cards[0:2],cards[2:7]))
print "----Testing 6-card hands----"
for k in sorted(hands_6.keys()):
    cards = hands_6[k]
    rank_6 = HandEvaluator.Six.evaluate_rank(cards)
    rank_5 = min(map(HandEvaluator.Five.evaluate_rank, combinations(cards,5)))
    print "Rank of %s is %s (%s expected)" % (k, rank_6, rank_5)
    print "Percentile of %s is %s" % (k, HandEvaluator.evaluate_hand(cards[0:2],cards[2:7]))
print "----Testing 7-card hands----"
for k in sorted(hands_7.keys()):
    cards = hands_7[k]
    rank_7 = HandEvaluator.Seven.evaluate_rank(cards)
    rank_5 = min(map(HandEvaluator.Five.evaluate_rank, combinations(cards,5)))
    print "Rank of %s is %s (%s expected)" % (k, rank_7, rank_5)
    print "Percentile of %s is %s" % (k, HandEvaluator.evaluate_hand(cards[0:2],cards[2:7]))