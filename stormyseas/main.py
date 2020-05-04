import cProfile

from stormyseas import profile_export
from stormyseas.solve import *

is_profile_enabled = True

input_ = open('../tests/input/problem_2.txt').read()

profile = cProfile.Profile()

if is_profile_enabled:
    profile.enable()

solution = Puzzle(input_).solve()
print('Solution has %d moves.' % solution.length())
print(solution)

if is_profile_enabled:
    profile.disable()
    profile_export.to_csv(profile, 'logs/profile.csv')
