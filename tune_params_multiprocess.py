from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import sys, itertools, random, fileinput, shutil, os, time
from multiprocessing import Pool

NUMBER_OF_PROCESSES = 4
# See bottom of file for parameter combinations and starting the game

def run_tournament(tournament_teams):
    # assume input is list -- this is different!
    if len(tournament_teams) == 1:
        return list(tournament_teams)[0]
    tournament_winners = []
    if len(tournament_teams) % 2 == 1:
        bye_team = random.choice(tournament_teams)
        tournament_teams.remove(bye_team)
        tournament_winners.append(bye_team)
    pool = Pool(processes=NUMBER_OF_PROCESSES)
    while len(tournament_teams) > 0:
        start_time = time.time()
        results = [None for i in xrange(NUMBER_OF_PROCESSES)]
        # Start all the processes, if necessary
        for i in xrange(NUMBER_OF_PROCESSES):
            if len(tournament_teams) > 0:
                pair = random.sample(tournament_teams, 2)
                # base name of this
                pair.append("tournament_%s" % (i,))
                tournament_teams.remove(pair[0])
                tournament_teams.remove(pair[1])
                results[i] = pool.apply_async(face_off, pair)
        # Wait for all processes to finish.
        # TODO: Is there a way around this?
        for i in xrange(NUMBER_OF_PROCESSES):
            if results[i]:
                tournament_winners.append(results[i].get())
        # print "Played %s matches in %.3f seconds" % (NUMBER_OF_PROCESSES, time.time() - start_time,)
    print "Teams left: %s" % (len(tournament_teams) + len(tournament_winners),)
    return run_tournament(tournament_winners)

# Have to pass name in. Make sure not to reuse names between concurrent
# processes, or you will have file access issues.
def face_off(p1_params, p2_params, base_name):
    p1_name = base_name + "_1"
    p2_name = base_name + "_2"
    p1_module_key = 'pokerbots.player.%s.%s' % (p1_name, p1_name,)
    p2_module_key = 'pokerbots.player.%s.%s' % (p2_name, p2_name,)
    p1_wins = 0
    p2_wins = 0
    generate_bot(p1_name, p1_params)
    generate_bot(p2_name, p2_params)
    # Must reload the bots, or you keep making the old ones
    # Must happen right after the code changes
    if p1_module_key in sys.modules:
        reload(sys.modules[p1_module_key])
    if p2_module_key in sys.modules:
        reload(sys.modules[p2_module_key])
    p1 = Pokerbot(p1_name)
    p2 = Pokerbot(p2_name)
    
    num_matches = 25
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
        # Use this to show progress
        # if i > 0 and (i + 1) % 10 == 0:
            # print "So far, of %s matches, %s won %s and %s won %s" % \
                # (i + 1, p1_name, p1_wins, p2_name, p2_wins,)
    print "%s %s - %s %s (%s matches)" % \
        ("(%s, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)" % p1_params, p1_wins,
        p2_wins, "(%s, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)" % p2_params,
        num_matches)
    sys.stdout.flush()
    if p1_wins > p2_wins:
        return p1_params
    else:
        return p2_params

def generate_bot(target_name, param_set):
    source_name = param_set[0]
    source_file_name = source_name + ".py"
    source_dir = os.path.join("pokerbots", "player", source_name)
    
    target_file_name = target_name + ".py"
    target_dir = os.path.join("pokerbots", "player", target_name)
    target_full_file_name = os.path.join(target_dir, target_file_name)
    target_init_py_name = os.path.join(target_dir, "__init__.py")
    target_hand_evaluator_name = os.path.join(target_dir, "hand_evaluator.py")

    # Check if the directory and three files we need exist:
    # __init__.py, target_name.py, hand_evaluator.py
    # If so, just edit in place. If not, copy the template over.
    # TODO: This test is not perfect! But it will save time.
    # We should really look if the files have content
    if not os.path.exists(target_dir) or not os.path.exists(target_full_file_name) or \
    not os.path.exists(target_init_py_name) or not os.path.exists(target_hand_evaluator_name):
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
            # TODO: Use all parameters
            print "    def __init__(self, param1=%s, param2=%s, param3=%s, param4=%s, param5=%s, param6=%s):" % param_set[1:]
        elif fileinput.filelineno() == 12:
            print "        self.name = \"%s\"" % (target_name,)
        else:
            print line,

def filter(team):
    # return True to keep, False to drop
    return True

if __name__ == '__main__':
    # p1_choices = (0.4, 0.45, 0.5, 0.55, 0.6)
    # p2_choices = (0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 1.0)
    # p3_choices = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    # p4_choices = (1, 2, 5, 10, 20, 30, 50, 100)
    # this is 3080 teams
    botnames = ["Template", "masterchefC", "bleedbot", "psychicbot"]
    p1 = [0.4, 0.5, 0.6, 0.7]
    p2 = [0.95]
    p3 = [0.3, 0.5, 0.7]
    p4 = [5, 10, 20]
    p5 = [0.3, 0.5, 0.7]
    p6 = [2, 8, 16]
    teams = list(itertools.product(botnames, p1, p2, p3, p4, p5, p6))
    best_team = run_tournament(teams)
    print best_team