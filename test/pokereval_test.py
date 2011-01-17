import sys
sys.path.append("../")
import random
import math
from itertools import combinations
import pokereval
from pokerbots.player.hand_evaluator_python import HandEvaluator
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
number_of_runs = 10
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

def _pokereval_evaluate_hand_bm(hand, board, iterations=None):
    hand = map(to_str, hand)
    board = map(to_str, board)
    for i in xrange(5 - len(board)):
        board.append("__")
    if iterations:
        return pe.poker_eval(game="holdem", pockets=[hand, [255,255]],
            dead=[], board=board, iterations=iterations)
    else:
        return pe.poker_eval(game="holdem", pockets=[hand, [255,255]],
            dead=[], board=board)

def pokereval_convergence(num_cards=7):
    for i in xrange(number_of_runs):
        cards = random.sample(deck, num_cards)
        hand = cards[0:2]
        board = cards[2:num_cards]
        for i in (100,300,500,1000,5000,None):
            if i:
                pe_result = _pokereval_evaluate_hand_bm(hand, board, iterations = i)
            else:
                pe_result = _pokereval_evaluate_hand_bm(hand, board)
            pe_win_pct = pe_result['eval'][0]['winhi'] / float(pe_result['info'][0])
            pe_ev = pe_result['eval'][0]['ev']
        
            # print pe_result
        
            print "PokerEval win pct is %s, EV is %s (%s iterations)" % (pe_win_pct,
                pe_ev, pe_result['info'][0])

def pokereval_results(num_cards=7, print_to_screen=False):
    pe = pokereval.PokerEval()
    to_str = lambda c: c.__str__()
    for i in xrange(number_of_runs):
        cards = random.sample(deck, num_cards)
        hand = cards[0:2]
        # hand = [Card(14,1), Card(14,2)]
        board = cards[2:num_cards]
        
        he_result = HandEvaluator.evaluate_hand(hand, board)
        pe_result = _pokereval_evaluate_hand_bm(hand, board, 1000)
        
        pe_win_pct = pe_result['eval'][0]['winhi'] / float(pe_result['info'][0])
        pe_ev = pe_result['eval'][0]['ev']
        
        # print pe_result
        
        #print "PokerEval win pct is %s, EV is %s (%s iterations)" % (pe_win_pct,
            #pe_ev, pe_result['info'][0])

# pokereval_results(5, print_to_screen=True)
pokereval_convergence(7)