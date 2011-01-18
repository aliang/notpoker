from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time
import sys
sys.path.append('pokerbots\player\\vivekbot')

p1 = Pokerbot('Template')
p2 = Pokerbot('vivekbot')

num_matches = 9

for i in range(num_matches):
    t = Table(p1, p2)
    t.play_match()
