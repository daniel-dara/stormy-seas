from cProfile import Profile
from importlib import resources

from stormyseas import Puzzle

from tests.performance import profile_export
from tests import input

# PyCharm bug (PY-42260)
# noinspection PyTypeChecker
puzzle_string = resources.read_text(input, 'problem_2.txt')

profile = Profile()
profile.enable()

solution = Puzzle(puzzle_string).solve()
print('Solution has %d steps and %d moves.' % (solution.step_count(), solution.move_count()))
print(solution)

profile.disable()
profile_export.csv(profile, 'logs/profile.csv')
