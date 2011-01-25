from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time


STUB_OUT_LOGGER = False

p1_name = 'masterchefC'
p2_name = 'masterchefC'
p1 = Pokerbot(p1_name)
p2 = Pokerbot(p2_name)
p1_wins = 0
p2_wins = 0
num_matches = 400

def stub(*args, **kwargs):
    pass

for i in range(num_matches):
    t = Table(p1, p2)
    if STUB_OUT_LOGGER:
        t.logger.action = stub
        t.logger.begin_hand = stub
        t.logger.blinds = stub
        t.logger.end = stub
        t.logger.file_one = stub
        t.logger.file_two = stub
        t.logger.preflop = stub
        t.logger.refund = stub
        t.logger.results = stub
        t.logger.showdown = stub
        t.logger.street = stub
        t.logger.time = stub
        t.logger.write_both = stub
        t.logger.write_one = stub
        t.logger.write_two = stub
    t.play_match()
    state = t.state()
    if state['players'][0]['stack'] == 800:
        p1_wins += 1
    else:
        p2_wins += 1
    if i > 0 and (i + 1) % 25 == 0:
        print "So far, of %s matches, %s won %s and %s won %s" % (i + 1, p1_name, p1_wins, p2_name, p2_wins,)
