from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time

p1 = Pokerbot('Template')
p2 = Pokerbot('masterchef')
# need to create a module name botname.botname containing the correct code.
# it's hardcoded sadly

num_matches = 10

for i in range(num_matches):
    t = Table(p1, p2)
    t.play_match()
