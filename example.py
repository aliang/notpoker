from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time

<<<<<<< HEAD
p1 = Pokerbot('Template')
p2 = Pokerbot('masterchef')
=======
# need to create a module name botname.botname containing the correct code.
# it's hardcoded sadly
p1 = Pokerbot('vivekbot')
p2 = Pokerbot('vivekbot')
>>>>>>> bc45e2f49e0a1208895805bd22618131df48c669

num_matches = 10

for i in range(num_matches):
    t = Table(p1, p2)
    t.play_match()
