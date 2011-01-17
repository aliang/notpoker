from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot

p1 = Pokerbot('VivekBot')
p2 = Pokerbot('VivekBot')

t = Table(p1, p2)

while t.p1.stack > 0 and t.p2.stack > 0:
    t.play()
