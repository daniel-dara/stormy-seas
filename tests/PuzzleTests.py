from unittest import TestCase

from unittest_data_provider import data_provider

from stormyseas.solve import *


# TODO: Fix old tests and write new ones.
class PuzzleTests(TestCase):
    @data_provider(lambda: (
        ("""
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##X#--#-
###X#-#--
""", False),
        ("""
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##-#X-#-
###-#X#--
""", True),
        ("""
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##-#XX#-
###-#-#--
""", False),
    ))
    def test_solved(self, input_: str, expected: str):
        puzzle = Puzzle(input_)
        self.assertEqual(expected, puzzle._initial_state.is_solved())

    @data_provider(lambda: (
            ("""
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##X#--#-
###X#-#--
""", """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
--##X#--#
-###X#-#-
"""),
            ("""
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#B#-##-
--#B#A#--
-##X#A-#-
###X#-#--
    """, """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
---#B#-##
---#B#A#-
--##X#A-#
-###X#-#-
    """),
    ))
    def test_move_right(self, input_: str, expected: str):
        puzzle = Puzzle(input_)
        red_boat = puzzle._initial_state.find_piece('X')
        self.assertEqual(expected.strip(), str(puzzle._initial_state.move(red_boat, Cardinal.RIGHT)))
