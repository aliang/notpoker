import sys

from pokereval import PokerEval
from pokerbots.engine.game import Card

class HandEvaluator:
    evaluator = PokerEval()
    
    preflop_win_percentages_suited = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.3598, 0.3682, 0.3784, 0.3766, 0.3814, 0.4026, 0.4241, 0.4484, 0.4738, 0.5017, 0.532, 0.5737],
        [0, 0, 0.3598, 0, 0.3863, 0.3968, 0.3953, 0.4003, 0.4087, 0.4325, 0.4568, 0.4823, 0.5101, 0.5405, 0.5821],
        [0, 0, 0.3682, 0.3863, 0, 0.4145, 0.4133, 0.4184, 0.427, 0.4385, 0.4653, 0.4906, 0.5185, 0.5488, 0.5903],
        [0, 0, 0.3784, 0.3968, 0.4145, 0, 0.4313, 0.4367, 0.4454, 0.4572, 0.4721, 0.4999, 0.5276, 0.5579, 0.5992],
        [0, 0, 0.3766, 0.3953, 0.4133, 0.4313, 0, 0.4536, 0.4623, 0.4742, 0.4894, 0.506, 0.536, 0.5664, 0.599],
        [0, 0, 0.3814, 0.4003, 0.4184, 0.4367, 0.4536, 0, 0.4793, 0.4912, 0.5064, 0.5232, 0.543, 0.5753, 0.6098],
        [0, 0, 0.4026, 0.4087, 0.427, 0.4454, 0.4623, 0.4793, 0, 0.5079, 0.5233, 0.5401, 0.5601, 0.5831, 0.6194],
        [0, 0, 0.4241, 0.4325, 0.4385, 0.4572, 0.4742, 0.4912, 0.5079, 0, 0.5402, 0.5566, 0.5766, 0.5998, 0.6277],
        [0, 0, 0.4484, 0.4568, 0.4653, 0.4721, 0.4894, 0.5064, 0.5233, 0.5402, 0, 0.5752, 0.5947, 0.6178, 0.6459],
        [0, 0, 0.4738, 0.4823, 0.4906, 0.4999, 0.506, 0.5232, 0.5401, 0.5566, 0.5752, 0, 0.6026, 0.6256, 0.6539],
        [0, 0, 0.5017, 0.5101, 0.5185, 0.5276, 0.536, 0.543, 0.5601, 0.5766, 0.5947, 0.6026, 0, 0.6339, 0.6621],
        [0, 0, 0.532, 0.5405, 0.5488, 0.5579, 0.5664, 0.5753, 0.5831, 0.5998, 0.6178, 0.6256, 0.6339, 0, 0.6704],
        [0, 0, 0.5737, 0.5821, 0.5903, 0.5992, 0.599, 0.6098, 0.6194, 0.6277, 0.6459, 0.6539, 0.6621, 0.6704, 0]
    ]
    
    preflop_win_percentages_unsuited = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.5033, 0.3229, 0.3319, 0.3428, 0.3406, 0.3458, 0.3682, 0.3909, 0.4165, 0.4434, 0.4729, 0.5051, 0.5492],
        [0, 0, 0.3229, 0.5368, 0.3514, 0.3625, 0.3607, 0.3659, 0.3747, 0.4001, 0.4259, 0.4527, 0.4821, 0.5142, 0.5584],
        [0, 0, 0.3319, 0.3514, 0.5702, 0.3815, 0.3801, 0.3854, 0.3944, 0.4067, 0.4349, 0.4618, 0.4912, 0.5232, 0.5672],
        [0, 0, 0.3428, 0.3625, 0.3815, 0.6032, 0.3994, 0.4051, 0.4143, 0.4266, 0.4424, 0.4717, 0.5011, 0.5331, 0.5769],
        [0, 0, 0.3406, 0.3607, 0.3801, 0.3994, 0.6328, 0.4232, 0.4323, 0.4449, 0.4608, 0.4784, 0.5102, 0.5421, 0.5768],
        [0, 0, 0.3458, 0.3659, 0.3854, 0.4051, 0.4232, 0.6623, 0.4505, 0.463, 0.479, 0.4968, 0.5176, 0.5518, 0.5883],
        [0, 0, 0.3682, 0.3747, 0.3944, 0.4143, 0.4323, 0.4505, 0.6915, 0.4809, 0.4971, 0.5149, 0.536, 0.5602, 0.5986],
        [0, 0, 0.3909, 0.4001, 0.4067, 0.4266, 0.4449, 0.463, 0.4809, 0.7205, 0.5153, 0.5324, 0.5536, 0.578, 0.6076],
        [0, 0, 0.4165, 0.4259, 0.4349, 0.4424, 0.4608, 0.479, 0.4971, 0.5153, 0.7501, 0.5524, 0.5728, 0.5973, 0.6271],
        [0, 0, 0.4434, 0.4527, 0.4618, 0.4717, 0.4784, 0.4968, 0.5149, 0.5324, 0.5524, 0.7747, 0.5813, 0.6057, 0.6355],
        [0, 0, 0.4729, 0.4821, 0.4912, 0.5011, 0.5102, 0.5176, 0.536, 0.5536, 0.5728, 0.5813, 0.7992, 0.6145, 0.6442],
        [0, 0, 0.5051, 0.5142, 0.5232, 0.5331, 0.5421, 0.5518, 0.5602, 0.578, 0.5973, 0.6057, 0.6145, 0.8239, 0.6531],
        [0, 0, 0.5492, 0.5584, 0.5672, 0.5769, 0.5768, 0.5883, 0.5986, 0.6076, 0.6271, 0.6355, 0.6442, 0.6531, 0.852]
    ]
    
    def card_to_str(card):
        """
        Convert this card to a string or number for pypoker-eval.
        Note that I don't check whether you passed a Card or the right string
        format!
        """
        if isinstance(card, str):
            return card
        return card.__str__()

    def str_to_card(card_string):
        """
        Convert this string to a pokerbots.engine.game.Card instance.
        Note that I don't check whether or not you passed the right format!
        """
        if isinstance(card_string, Card):
            return card
        rank_str = card_string[0].lower()
        suit_str = card_string[1].lower()
        rank = 2
        suit = 1
        if rank_str == "t":
            rank = 10
        elif rank_str == "j":
            rank = 11
        elif rank_str == "q":
            rank = 12
        elif rank_str == "k":
            rank = 13
        elif rank_str == "a":
            rank = 14
        if suit_str == "s":
            suit = 1
        elif suit_str == "h":
            suit = 2
        elif suit_str == "d":
            suit = 3
        elif suit_str == "c":
            suit = 4
        return Card(rank,suit)
    
    def evaluate_hand(hand, board=[], iterations=1000):
        """
        Return winning percentage of your hand, with ties counted as 0.5
        Includes Monte-Carlo simulation of running the board.
        Includes trying all possible opponent hands.
        Arguments:
        hand: your hand
        board: the board if any
        iterations: number of times to simulate
        """
        # If the board is determined, there's only 990 hands to run,
        # so run them all
        if len(board) == 5:
            # convert to pypoker-eval format
            hand = map(HandEvaluator.card_to_str, hand)
            board = map(HandEvaluator.card_to_str, board)
            poker_eval_result = HandEvaluator.evaluator.poker_eval(game="holdem",
                pockets=[hand, [255,255]], dead=[],
                board=board)
        elif len(board) == 0:
            # Use a lookup table, because this has been done before
            if hand[0].suit == hand[1].suit:
                return HandEvaluator.preflop_win_percentages_suited[hand[0].rank][hand[1].rank]
            else:
                return HandEvaluator.preflop_win_percentages_unsuited[hand[0].rank][hand[1].rank]
        else:
            hand = map(HandEvaluator.card_to_str, hand)
            board = map(HandEvaluator.card_to_str, board)
            # Fill the rest of the board with 255s
            for i in xrange(5 - len(board)):
                board.append(255)
            poker_eval_result = HandEvaluator.evaluator.poker_eval(game="holdem",
                pockets=[hand, [255,255]], dead=[],
                board=board,
                iterations=iterations)
        
        # Ok, we have stats. Calculate win pct, with ties as 0.5 weight
        return (poker_eval_result['eval'][0]['winhi'] + \
                0.5 * poker_eval_result['eval'][0]['tiehi']) / \
                float(poker_eval_result['info'][0])

    card_to_str = staticmethod(card_to_str)
    str_to_card = staticmethod(str_to_card)
    evaluate_hand = staticmethod(evaluate_hand)