from stormyseas.solve import *

input_ = """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##X#--#-
###X#-#--
"""

solution = Puzzle(input_).solve()

print('Solution has ' + str(solution.length()) + ' moves.')
print(solution)
