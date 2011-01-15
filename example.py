from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot

p1 = Pokerbot('AlvinBot')
p2 = Pokerbot('AlvinBot')

t = Table(p1, p2)

for i in xrange(50):
    while t.p1.stack > 0 and t.p2.stack > 0:
        t.play()
