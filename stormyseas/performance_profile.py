import cProfile

from stormyseas import profile_export
from stormyseas.puzzle import *

is_profile_enabled = True

input_ = open('../tests/input/problem_2.txt').read()

profile = cProfile.Profile()

if is_profile_enabled:
    profile.enable()

solution = Puzzle(input_).solve()
print('Solution has %d steps and %d moves.' % (solution.step_count(), solution.move_count()))
print(solution)

if is_profile_enabled:
    profile.disable()
    profile_export.to_csv(profile, 'logs/profile.csv')
