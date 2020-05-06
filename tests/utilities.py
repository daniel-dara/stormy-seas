from importlib import resources
from unittest import TestCase

from stormyseas import Solution
from tests import input


class StormySeasTest(TestCase):
    def assertSolutionEqual(self, solution_string: str, solution: Solution) -> bool:
        expected_move_strings = solution_string.split(', ')
        actual_move_strings = [str(move) for move in solution.moves]
        self.assertCountEqual(expected_move_strings, actual_move_strings, '\nactual list: ' + str(actual_move_strings))
        self.assertEqual(solution_string, str(solution))


def read_test_file(filename: str) -> str:
    # PyCharm bug (PY-42260)
    # noinspection PyTypeChecker
    return resources.read_text(input, filename)
