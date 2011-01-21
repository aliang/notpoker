from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import sys, itertools, random, fileinput, shutil, os, time
from multiprocessing import Pool

def run_tournament(tournament_teams):
    # assume input is list -- this is different!
    if len(tournament_teams) == 1:
        return list(tournament_teams)[0]
    tournament_winners = []
    if len(tournament_teams) % 2 == 1:
        bye_team = random.choice(tournament_teams)
        tournament_teams.remove(bye_team)
        tournament_winners.append(bye_team)
    pool = Pool(processes=4)
    while len(tournament_teams) > 0:
        start_time = time.time()
        result1 = None
        result2 = None
        result3 = None
        result4 = None
        if len(tournament_teams) > 0:
            pair1 = random.sample(tournament_teams, 2)
            pair1.append("tournament1")
            tournament_teams.remove(pair1[0])
            tournament_teams.remove(pair1[1])
            result1 = pool.apply_async(face_off, pair1)
        if len(tournament_teams) > 0:
            pair2 = random.sample(tournament_teams, 2)
            pair2.append("tournament2")
            tournament_teams.remove(pair2[0])
            tournament_teams.remove(pair2[1])
            result2 = pool.apply_async(face_off, pair2)
        if len(tournament_teams) > 0:
            pair3 = random.sample(tournament_teams, 2)
            pair3.append("tournament3")
            tournament_teams.remove(pair3[0])
            tournament_teams.remove(pair3[1])
            result3 = pool.apply_async(face_off, pair3)
        if len(tournament_teams) > 0:
            pair4 = random.sample(tournament_teams, 2)
            pair4.append("tournament4")
            tournament_teams.remove(pair4[0])
            tournament_teams.remove(pair4[1])
            result4 = pool.apply_async(face_off, pair4)
        # need to wait for all processes to finish.
        # TODO: Is there a way around this?
        if result1:
            tournament_winners.append(result1.get())
        if result2:
            tournament_winners.append(result2.get())
        if result3:
            tournament_winners.append(result3.get())
        if result4:
            tournament_winners.append(result4.get())
        # print "Played 4 matches in %.3f seconds" % (time.time() - start_time,)
    # print "Teams left: %s" % (len(tournament_teams) + len(tournament_winners),)
    return run_tournament(tournament_winners)

# Have to pass name in. Make sure not to reuse names between concurrent
# processes, or you will have file access issues.
def face_off(p1_params, p2_params, base_name):
    p1_name = base_name + "1"
    p2_name = base_name + "2"
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
        ("(%.3f, %.3f, %.3f, %.3f)" % p1_params, p1_wins,
        p2_wins, "(%.3f, %.3f, %.3f, %.3f)" % p2_params,
        num_matches)
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
    target_init_py_name = os.path.join(target_dir, "__init__.py")
    target_hand_evaluator_name = os.path.join(target_dir, "hand_evaluator.py")

    # Check if the directory and three files we need exist:
    # __init__.py, target_name.py, hand_evaluator.py
    # If so, just edit in place. If not, copy the template over.
    # TODO: This test is not perfect! But it will save time.
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
            print "    def __init__(self, param1=%s, param2=%s, param3=%s, param4=%s):" % param_set
        elif fileinput.filelineno() == 12:
            print "        self.name = \"%s\"" % (target_name,)
        else:
            print line,

if __name__ == '__main__':
    p1_choices = (0.4, 0.45, 0.5, 0.55, 0.6)
    p2_choices = (0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 1.0)
    p3_choices = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    p4_choices = (1, 2, 5, 10, 20, 30, 50, 100)
    # this is 3080 teams
    teams = list(itertools.product(p1_choices, p2_choices, p3_choices, p4_choices))
    best_team = run_tournament(teams)