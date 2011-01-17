import sys
from pstats import Stats

s = Stats(sys.argv[1])
s.sort_stats("cum").print_stats(sys.argv[2])