from unittest import TestCase

from unittest_data_provider import data_provider

from stormyseas.solve import *


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
--#B-####
--#B#-##-
--#B#A#--
-##X#A-#-
###X#-#--
    """, """
--#-#-###
--#-###-#
--#-##-##
--#-B####
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

    @data_provider(lambda: (
        ('input/problem_1_initial.txt', 4, Cardinal.LEFT, 'input/problem_1_step_1.txt'),
        ('input/problem_1_step_1.txt', 4, Cardinal.LEFT, 'input/problem_1_step_2.txt'),
        ('input/problem_1_step_2.txt', 3, Cardinal.LEFT, 'input/problem_1_step_3.txt'),
        ('input/problem_1_step_3.txt', 3, Cardinal.LEFT, 'input/problem_1_step_4.txt'),
        ('input/problem_1_step_4.txt', 'X', Cardinal.UP, 'input/problem_1_step_5.txt'),
        ('input/problem_1_step_5.txt', 'X', Cardinal.UP, 'input/problem_1_step_6.txt'),
        ('input/problem_1_step_6.txt', 'X', Cardinal.UP, 'input/problem_1_step_7.txt'),
        ('input/problem_1_step_7.txt', 'X', Cardinal.RIGHT, 'input/problem_1_step_8.txt'),
        ('input/problem_1_step_8.txt', 'X', Cardinal.RIGHT, 'input/problem_1_step_9.txt'),
        ('input/problem_1_step_9.txt', 5, Cardinal.LEFT, 'input/problem_1_step_10.txt'),
        ('input/problem_1_step_10.txt', 5, Cardinal.LEFT, 'input/problem_1_step_11.txt'),
        ('input/problem_1_step_11.txt', 6, Cardinal.LEFT, 'input/problem_1_step_12.txt'),
        ('input/problem_1_step_12.txt', 7, Cardinal.RIGHT, 'input/problem_1_step_13.txt'),
        ('input/problem_1_step_13.txt', 7, Cardinal.RIGHT, 'input/problem_1_step_14.txt'),
        ('input/problem_1_step_14.txt', 'X', Cardinal.DOWN, 'input/problem_1_step_15.txt'),
        ('input/problem_1_step_15.txt', 'X', Cardinal.DOWN, 'input/problem_1_step_16.txt'),
        ('input/problem_1_step_16.txt', 'X', Cardinal.DOWN, 'input/problem_1_step_17.txt'),
    ))
    def test_problem_1(self, input_file: str, id_: str, direction: Direction, expected_file: str):
        print(input_file)

        with open(input_file) as input_, open(expected_file) as expected:
            puzzle = Puzzle(input_.read())
            piece = puzzle._initial_state.find_piece(id_)
            next_state = puzzle._initial_state.move(piece, direction)
            self.assertTrue(next_state.is_valid())
            self.assertEqual(expected.read().strip(), str(next_state))

            if expected_file == 'input/problem_1_step_17.txt':
                self.assertTrue(next_state.is_solved())
            else:
                self.assertFalse(next_state.is_solved())

    def test_problem_1_continuous_moves(self):
        moves = [
            (4, Cardinal.LEFT),
            (4, Cardinal.LEFT),
            (3, Cardinal.LEFT),
            (3, Cardinal.LEFT),
            ('X', Cardinal.UP),
            ('X', Cardinal.UP),
            ('X', Cardinal.UP),
            ('X', Cardinal.RIGHT),
            ('X', Cardinal.RIGHT),
            (5, Cardinal.LEFT),
            (5, Cardinal.LEFT),
            (6, Cardinal.LEFT),
            (7, Cardinal.RIGHT),
            (7, Cardinal.RIGHT),
            ('X', Cardinal.DOWN),
            ('X', Cardinal.DOWN),
            ('X', Cardinal.DOWN),
        ]

        with open('input/problem_1_initial.txt') as input_:
            puzzle = Puzzle(input_.read())

        state = puzzle._initial_state

        for id_, direction in moves:
            self.assertFalse(state.is_solved())

            piece = state.find_piece(id_)
            state = state.move(piece, direction)

            self.assertTrue(state.is_valid())

        self.assertTrue(state.is_solved())

    def test_solve_from_step_12(self):
        with open('input/problem_1_step_13.txt') as input_:
            puzzle = Puzzle(input_.read())
            solution = puzzle.solve()
            self.assertEqual(4, solution.length())
