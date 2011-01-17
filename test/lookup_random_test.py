import sys
sys.path.append("../")
from pokerbots.engine.game import Card
from pokerbots.player.hand_evaluator import HandEvaluator
from itertools import combinations
import random

deck = [
    Card(2,1), Card(2,2), Card(2,3), Card(2,4),
    Card(3,1), Card(3,2), Card(3,3), Card(3,4),
    Card(4,1), Card(4,2), Card(4,3), Card(4,4),
    Card(5,1), Card(5,2), Card(5,3), Card(5,4),
    Card(6,1), Card(6,2), Card(6,3), Card(6,4),
    Card(7,1), Card(7,2), Card(7,3), Card(7,4),
    Card(8,1), Card(8,2), Card(8,3), Card(8,4),
    Card(9,1), Card(9,2), Card(9,3), Card(9,4),
    Card(10,1), Card(10,2), Card(10,3), Card(10,4),
    Card(11,1), Card(11,2), Card(11,3), Card(11,4),
    Card(12,1), Card(12,2), Card(12,3), Card(12,4),
    Card(13,1), Card(13,2), Card(13,3), Card(13,4),
    Card(14,1), Card(14,2), Card(14,3), Card(14,4)
]

number_of_runs = 1000

def test_6():
    for i in xrange(number_of_runs):
        hand = random.sample(deck, 6)
        possible_hands = combinations(hand, 5)
        rank_5 = min(map(HandEvaluator.Five.evaluate_rank, possible_hands))
        rank_6 = HandEvaluator.Six.evaluate_rank(hand)
        if rank_5 != rank_6:
            print "Got rank %s from Six.evaluate_rank (%s expected)" % (rank_6, rank_5)
            print hand

def test_7():
    for i in xrange(number_of_runs):
        hand = random.sample(deck, 7)
        possible_hands = combinations(hand, 5)
        rank_5 = min(map(HandEvaluator.Five.evaluate_rank, possible_hands))
        rank_7 = HandEvaluator.Seven.evaluate_rank(hand)
        if rank_5 != rank_7:
            print "Got rank %s from Seven.evaluate_rank (%s expected)" % (rank_7, rank_5)
            print hand

test_6()
test_7()