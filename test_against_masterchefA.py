from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time
import sys

p1_name = 'masterchefA'
p2_name = sys.argv[1]
p1_wins = 0
p2_wins = 0
p1 = Pokerbot(p1_name)
p2 = Pokerbot(p2_name)

num_matches = 100

for i in range(num_matches):
    t = Table(p1, p2)
    t.play_match()
    # To find the winner, read the state. Who has 800 chips?
    # TODO: We assume no timeout!
    state = t.state()
    if state['players'][0]['stack'] == 800:
        p1_wins += 1
    else:
        p2_wins += 1

print "Out of %s matches, %s won %s and %s won %s" % (num_matches, p1_name, p1_wins, p2_name, p2_wins,)