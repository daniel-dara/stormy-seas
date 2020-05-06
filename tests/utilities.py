from enum import Enum
from importlib import resources
from types import ModuleType
from unittest import TestCase

from stormyseas import Solution
from tests.input import cards


class StormySeasTest(TestCase):
    def assertSolutionEqual(self, solution_string: str, solution: Solution) -> bool:
        expected_move_strings = solution_string.split(', ')
        actual_move_strings = [str(move) for move in solution.moves]
        self.assertCountEqual(expected_move_strings, actual_move_strings, '\nactual list: ' + str(actual_move_strings))
        self.assertEqual(solution_string, str(solution))


class InputFile(Enum):
    CARD_3 = cards, 'card_3'

    def read(self) -> str:
        return read_file(*self.value)


def read_file(module: ModuleType, name: str) -> str:
    return resources.read_text(module, name + '.txt')
