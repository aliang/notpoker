from pokereval import PokerEval

class HandEvaluator:
    evaluator = PokerEval()
    to_str = lambda c: c.__str__()
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
    
    preflop_win_percentages_suited = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # rank 0 (not used)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # rank 1 (not used)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    
    preflop_win_percentages_unsuited = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # rank 0
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # rank 1
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 2
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    
    def evaluate_hand(hand, board, iterations=1000):
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
            hand = map(to_str, hand)
            board = map(to_str, board)
            poker_eval_result = evaluator.poker_eval(game="holdem",
                pockets=[hand, [255,255]], dead=[],
                board=board)
        elif len(board) == 0:
            # Use a lookup table, because this has been done before
            if hand[0].suit == hand[1].suit:
                return preflop_win_percentages_suited[hand[0].rank][hand[1].rank]
            else:
                return preflop_win_percentages_unsuited[hand[0].rank][hand[1].rank]
        else:
            hand = map(to_str, hand)
            board = map(to_str, board)
            # Fill the rest of the board with 255s
            for i in xrange(5 - len(board)):
                board.append(255)
            poker_eval_result = evaluator.poker_eval(game="holdem",
                pockets=[hand, [255,255]], dead=[],
                board=board,
                iterations=iterations)
        
        # Ok, we have stats. Calculate win pct, with ties as 0.5 weight
        return (pe_result['eval'][0]['winhi'] + \
                0.5 * pe_result['eval'][0]['tiehi']) / \
                float(pe_result['info'][0])
    evaluate_hand = staticmethod(evaluate_hand)