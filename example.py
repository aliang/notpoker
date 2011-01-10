from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot

p1 = Pokerbot('Template')
p2 = Pokerbot('Template')

t = Table(p1, p2)

while t.p1.stack > 0 and t.p2.stack > 0:
    t.play()

t.logger.file_one.close()
t.logger.file_two.close()
