from pokerbots.engine.game import Card
from pokerbots.player.hand_evaluator import HandEvaluator
from itertools import combinations
import random

for i in xrange(100):
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

    random.shuffle(deck)
    h1 = deck.pop()
    h2 = deck.pop()
    c1 = deck.pop()
    c2 = deck.pop()
    c3 = deck.pop()

    your_hand = (h1, h2,)
    flop = (c1, c2, c3,)
    your_rank = HandEvaluator.evaluate_hand(your_hand + flop)
    possible_opponent_hands = combinations(deck, 2)
    counter = 0
    for hand in possible_opponent_hands:
        counter += 1
        opponent_rank = HandEvaluator.evaluate_hand(hand + flop)

    turn = (deck.pop(),)
    your_rank = HandEvaluator.evaluate_hand(your_hand + flop + turn)
    counter = 0
    possible_opponent_hands = combinations(deck, 2)
    for hand in possible_opponent_hands:
        counter += 1
        opponent_rank = HandEvaluator.evaluate_hand(hand + flop)

    river = (deck.pop(),)
    your_rank = HandEvaluator.evaluate_hand(your_hand + flop + turn + river)
    counter = 0
    possible_opponent_hands = combinations(deck, 2)
    for hand in possible_opponent_hands:
        counter += 1
        opponent_rank = HandEvaluator.evaluate_hand(hand + flop)