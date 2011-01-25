from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time

p1_name = 'trickybotB'
p2_name = 'trickybot'
p1 = Pokerbot(p1_name)
p2 = Pokerbot(p2_name)
p1_wins = 0
p2_wins = 0
num_matches = 400

for i in range(num_matches):
    t = Table(p1, p2)
    t.play_match()
    state = t.state()
    if state['players'][0]['stack'] == 800:
        p1_wins += 1
    else:
        p2_wins += 1
    if i > 0 and (i + 1) % 25 == 0:
        print "So far, of %s matches, %s won %s and %s won %s" % (i + 1, p1_name, p1_wins, p2_name, p2_wins,)
