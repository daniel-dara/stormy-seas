import cProfile

from stormyseas import profile_export
from stormyseas.solve import *

is_profile_enabled = True
# noinspection PyProtectedMember
search_type = Puzzle._SearchType.SHORTEST

input_ = open('../tests/input/problem_2.txt').read()

profile = cProfile.Profile()

if is_profile_enabled:
    profile.enable()

# noinspection PyProtectedMember
if search_type == Puzzle._SearchType.SHORTEST:
    solution = Puzzle(input_).shortest_solution()
    print('Solution has %d moves.' % solution.length())
    print(solution.notation())
else:
    solutions = Puzzle(input_).all_solutions()
    print('Found %d solutions.' % len(solutions))

    shortest_solution = min(solutions, key=lambda sol: sol.length())
    print('The shortest solution has %d moves.' % shortest_solution.length())

    longest_solution = max(solutions, key=lambda sol: sol.length())
    print('The longest solution has %d moves.' % longest_solution.length())

if is_profile_enabled:
    profile.disable()
    profile_export.to_csv(profile, 'logs/profile.csv')
