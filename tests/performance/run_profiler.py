from cProfile import Profile

from stormyseas import Puzzle

from tests.performance import profile_export
from tests.utilities import InputFile

profile = Profile()
profile.enable()

solution = Puzzle(InputFile.CARD_3.read()).solve()
print('Solution has %d steps and %d moves.' % (solution.step_count(), solution.move_count()))
print(solution)

profile.disable()
profile_export.csv(profile, 'logs/profile.csv')
