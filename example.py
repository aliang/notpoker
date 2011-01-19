from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from pokerbots.player.vivekbot import vivekbot
import time

p1 = Pokerbot('Template')
p2 = Pokerbot('vivekbot')

num_matches = 100

for i in range(num_matches):
    t = Table(p1, p2)
    t.play_match()
