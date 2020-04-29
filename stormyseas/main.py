import cProfile

from stormyseas import profile_export
from stormyseas.solve import *

input_ = """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-###-#
-##X##-#-
###X###--
"""

profile = cProfile.Profile()
profile.enable()

solution = Puzzle(input_).solve()
print('Solution has ' + str(solution.length()) + ' moves.')
print(solution)

profile.disable()
profile_export.to_csv(profile, 'profile.csv')

