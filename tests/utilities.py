from enum import Enum, auto
from importlib import resources
from types import ModuleType
from unittest import TestCase

from stormyseas import Solution
from tests.assets import cards


class StormySeasTest(TestCase):
    def assertSolutionEqual(self, solution_string: str, solution: Solution) -> bool:
        expected_move_strings = solution_string.split(', ')
        actual_move_strings = [str(move) for move in solution.moves]
        self.assertCountEqual(expected_move_strings, actual_move_strings, '\nactual list: ' + str(actual_move_strings))
        self.assertEqual(solution_string, str(solution))


class Asset(Enum):
    CARD_3 = auto()
    CARD_10 = auto()
    CARD_31 = auto()

    @property
    def input(self) -> str:
        return self._read('.in')

    @property
    def output(self) -> str:
        return self._read('.out')

    def _read(self, suffix: str) -> str:
        return read_file(cards, self.name.lower() + suffix)


def read_file(module: ModuleType, file_name: str) -> str:
    return resources.read_text(module, file_name)
