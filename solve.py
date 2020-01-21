#!/usr/local/bin/python3
from src.Puzzle import Puzzle

# This input string represents the initial state of the puzzle.
# dashes (-) are open spaces
# number signs (#) are blocked spaces
# integers are boats, the boat trying to escape is the 0-boat
puzzle_input = """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##0#--#-
###0#-#--
"""

puzzle = Puzzle(puzzle_input)

print('Initial state:\n' + puzzle.get_state() + '\n')

print('Can this puzzle be solved?', 'Yes' if puzzle.is_solvable() else 'No')
