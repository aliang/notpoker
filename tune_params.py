from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import sys
import itertools
import random
import fileinput
import shutil
import os
import math
import time

def run_tournament(tournament_teams):
    # assume input is set
    if len(tournament_teams) == 1:
        return tournament_teams.pop()
    tournament_winners = set()
    if len(tournament_teams) % 2 == 1:
        bye_team = tournament_teams.pop()
        tournament_winners.add(bye_team)
    while len(tournament_teams) > 0:
        pair = random.sample(tournament_teams, 2)
        tournament_teams = tournament_teams - set(pair)
        # replace with a real way of choosing winners
        winner = face_off(*pair)
        tournament_winners.add(winner)
        print "Teams left: %s" % (len(tournament_teams) + len(tournament_winners),)
    return run_tournament(tournament_winners)

def face_off(p1_params, p2_params):
    p1_name = "tournament1"
    p2_name = "tournament2"
    p1_wins = 0
    p2_wins = 0
    generate_bot(p1_name, p1_params)
    generate_bot(p2_name, p2_params)
    p1 = Pokerbot(p1_name)
    p2 = Pokerbot(p2_name)
    
    num_matches = 25
    start_time = time.time()
    for i in range(num_matches):
        t = Table(p1, p2)
        t.play_match()
        # To find the winner, read the state. Who has 800 chips?
        # TODO: We assume no timeout!
        state = t.state()
        if state['players'][0]['stack'] == 800:
            p1_wins += 1
        else:
            p2_wins += 1
        # if i > 0 and (i + 1) % 10 == 0:
            # print "So far, of %s matches, %s won %s and %s won %s" % \
                # (i + 1, p1_name, p1_wins, p2_name, p2_wins,)

    print "%s matches: %s won %s and %s won %s in %s seconds" % \
        (num_matches, p1_name, p1_wins, p2_name, p2_wins, round(time.time() - start_time, 2),)
    if p1_wins > p2_wins:
        return p1_params
    else:
        return p2_params

def generate_bot(target_name, param_set):
    source_name = "masterchef_template"
    source_file_name = source_name + ".py"
    source_dir = os.path.join("pokerbots", "player", source_name)
    
    target_file_name = target_name + ".py"
    target_dir = os.path.join("pokerbots", "player", target_name)
    target_full_file_name = os.path.join(target_dir, target_file_name)

    # first, delete any existing bot
    shutil.rmtree(target_dir, True)
    # copy the new bot over
    shutil.copytree(source_dir, target_dir)
    # rename the template file to the final file
    os.rename(
        os.path.join(target_dir, source_file_name),
        target_full_file_name
    )

    # also need to replace the line where we create a bot
    # commas after print statement are important!
    # TODO: This is really fragile, should match regex too
    for line in fileinput.input(target_full_file_name, inplace=1):
        if fileinput.filelineno() == 6:
            print "class %s:" % (target_name,)
        elif fileinput.filelineno() == 7:
            print "    def __init__(self, param1=%s, param2=%s, param3=%s, param4=%s):" % param_set
        elif fileinput.filelineno() == 12:
            print "        self.name = \"%s\"" % (target_name,)
        else:
            print line,

p1_choices = (0.4, 0.45, 0.5, 0.55, 0.6)
p2_choices = (0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 1.0)
p3_choices = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
p4_choices = (1, 2, 5, 10, 20, 30, 50, 100)
# this is 3080 teams

# figure out number of play-in teams
teams = set(itertools.product(p1_choices, p2_choices, p3_choices, p4_choices))
best_team = run_tournament(teams)