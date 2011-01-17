import sys
sys.path.append("../")
import random
from itertools import combinations
import pokereval
from pokerbots.player.hand_evaluator import HandEvaluator
from pokerbots.engine.game import Card

deck = set((
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
))

pe = pokereval.PokerEval()
number_of_runs = 100
to_str = lambda c: c.__str__()

def pokereval_5_bm():
    for i in xrange(number_of_runs):
        cards = random.sample(deck, 5)
        hand = map(to_str, cards[0:2])
        board = map(to_str, cards[2:5])
        pe.poker_eval(game="holdem", pockets=[hand, [255,255]],
            dead=[], board=board)       

def pokereval_winners_5_bm():
    for i in xrange(number_of_runs):
        cards = random.sample(deck, 5)
        hand = map(to_str, cards[0:2])
        board = map(to_str, cards[2:5])
        possible_opponent_hands = list(combinations(deck - set(cards), 2))
        for opponent_hand in possible_opponent_hands:
            ohand = map(to_str, opponent_hand)
            pe_result = pe.winners(game="holdem", pockets=[hand, ohand],
                dead=[], board=board)
            hands_beaten = 0
            if pe_result['hi'][0] == 0:
                # player won this iteration
                hands_beaten += 1
            elif len(pe_result['hi']) == 2: # draw
                hands_beaten += 0.5
        float(hands_beaten) / len(possible_opponent_hands)

def handevaluator_5_bm():
    for i in xrange(number_of_runs):
        cards = random.sample(deck, 5)
        hand = cards[0:2]
        board = cards[2:5]
        HandEvaluator.evaluate_hand(hand, board)

def _pokereval_evaluate_hand_bm(cards):
    hand = map(to_str, cards[0:2])
    board = map(to_str, cards[2:7])
    return pe.poker_eval(game="holdem", pockets=[hand, [255,255]],
        dead=[], board=board)

def _winners_evaluate_hand_bm(cards):
    hand = map(to_str, cards[0:2])
    board = map(to_str, cards[2:7])
    possible_opponent_hands = list(combinations(deck - set(cards), 2))
    hands_beaten = 0
    for opponent_hand in possible_opponent_hands:
        ohand = map(to_str, opponent_hand)
        per = pe.winners(game="holdem", pockets=[hand, ohand],
            dead=hand + ohand, board=board)
        if len(per['hi']) == 2: # draw
            hands_beaten += 0.5
        elif per['hi'][0] == 0:
            # player won this iteration
            hands_beaten += 1
    return float(hands_beaten) / len(possible_opponent_hands)

def pokereval_results(print_to_screen=False):
    pe = pokereval.PokerEval()
    to_str = lambda c: c.__str__()
    for i in xrange(number_of_runs):
        cards = random.sample(deck, 7)
        hand = cards[0:2]
        board = cards[2:7]
        
        he_result = HandEvaluator.evaluate_hand(hand, board)
        pe_result = _pokereval_evaluate_hand_bm(cards)
        pe_winners = _winners_evaluate_hand_bm(cards)
        
        if print_to_screen:
            print "PokerEval.poker_eval got %s, .winners got %s, HandEvaluator got %s" % \
                (pe_result['eval'][0]['ev']/1000.0, pe_winners, he_result)

pokereval_results()