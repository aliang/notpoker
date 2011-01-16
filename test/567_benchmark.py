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

def eval_6_with_5():
    for i in xrange(number_of_runs):
        turn = random.sample(deck, 6)
        possible_hands = combinations(turn, 5)
        rank = min(map(HandEvaluator.Five.evaluate_rank, possible_hands))

def eval_6_with_6():
    for i in xrange(number_of_runs):
        turn = random.sample(deck, 6)
        rank = HandEvaluator.Six.evaluate_rank(turn)

def eval_7_with_5():
    for i in xrange(number_of_runs):
        river = random.sample(deck, 7)
        possible_hands = combinations(river, 5)
        rank = min(map(HandEvaluator.Five.evaluate_rank, possible_hands))

def eval_7_with_6():
    for i in xrange(number_of_runs):
        river = random.sample(deck, 7)
        possible_hands = combinations(river, 6)
        rank = min(map(HandEvaluator.Six.evaluate_rank, possible_hands))

def eval_7_with_7():
    for i in xrange(number_of_runs):
        river = random.sample(deck, 7)
        rank = HandEvaluator.Seven.evaluate_rank(river)

eval_6_with_5()
eval_6_with_6()
eval_7_with_5()
eval_7_with_6()
eval_7_with_7()