import random
import fileinput
import shutil
import sys
import os
# We work with argv[1]. Copy masterchefA to new location
target_file = os.path.join(sys.argv[1], "%s.py" % (sys.argv[1],))

shutil.copytree("masterchefA", "%s" % (sys.argv[1],))
os.rename(os.path.join(sys.argv[1], "masterchefA.py"), target_file)

# generate random numbers
p1 = round(random.random() * 2, 2)
p2 = round(random.random(), 2)
p3 = round(random.random(), 2)
p4 = round(random.random(), 2)

# also need to replace the line where we create a bot
# commas after print statement are important!
# TODO: This is really fragile, should match regex too
for line in fileinput.input(target_file, inplace=1):
    if fileinput.filelineno() == 6:
        print "class %s:" % (sys.argv[1],)
    elif fileinput.filelineno() == 7:
        print "    def __init__(self, param1=%s, param2=%s, param3=%s, param4=%s):" % (p1, p2, p3, p4,),
    elif fileinput.filelineno() == 13:
        print "        self.name = \"testchef\""
    else:
        print line,