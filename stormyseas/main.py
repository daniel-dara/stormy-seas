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

is_profile_enabled = True

profile = cProfile.Profile()

if is_profile_enabled:
    profile.enable()

solution = Puzzle(input_).solve()
print('Solution has ' + str(solution.length()) + ' moves.')
print(solution)

if is_profile_enabled:
    profile.disable()
    profile_export.to_csv(profile, 'profile.csv')

