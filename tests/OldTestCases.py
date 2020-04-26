from unittest import TestCase

from unittest_data_provider import data_provider

from stormyseas.solve import *

# TODO: Fix old tests and write new ones.
class TestCases(TestCase):
    @data_provider(lambda: (
        ([Move(Wave(6), Cardinal.RIGHT, 1)], '6R1'),
        ([Move(Boat('H'), Cardinal.DOWN, 2)], 'HD2'),
        ([Move(Boat('X'), Rotation.COUNTER_CLOCKWISE, 90)], 'X@'),
        ([Move(Boat('X'), Rotation.COUNTER_CLOCKWISE, 180)], 'X@@'),
        (
             [
                 Move(Boat('X'), Rotation.COUNTER_CLOCKWISE, 180),
                 Move(Wave(3), Cardinal.UP, 1),
                 Move(Boat('Z'), Cardinal.LEFT, 2),
                 Move(Boat('X'), Rotation.COUNTER_CLOCKWISE, 90),
             ],
             'X@@, 3U1, ZL2, X@'
        ),
    ))
    def test_valid_moves_and_solution_strings(self, moves: List[Move], expected: str):
        self.assertEqual(expected, str(Solution(moves)))

    @data_provider(lambda: (
        (Wave(6), Rotation.COUNTER_CLOCKWISE, 90),
        (Boat('H'), Rotation.COUNTER_CLOCKWISE, 89),
    ))
    def test_invalid_moves(self, piece: Piece, direction: Direction, distance: int):
        with self.assertRaises(ValueError):
            Move(piece, direction, distance)
