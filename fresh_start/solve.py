from enum import Enum
from typing import List


class Piece:
    def __init__(self, id_: str):
        self.id = id_


class Wave(Piece):
    def __init__(self, id_: int):
        super().__init__(str(id_))


class Boat(Piece):
    pass


class Direction:
    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance using Solution Notation."""
        pass


class Cardinal(Direction, Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def shorthand(self, distance: int) -> str:
        """Returns a single character representation of the current direction and appends the given distance."""
        return self.value + str(distance)


class Rotation(Direction, Enum):
    # There is no corresponding CLOCKWISE value because Solution Notation uses only the counter-clockwise direction.
    COUNTER_CLOCKWISE = 0

    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance."""
        return '@@' if distance == 180 else '@'


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self.piece = piece
        self.direction = direction
        self.distance = distance

        if isinstance(piece, Wave) and isinstance(direction, Rotation):
            raise ValueError('Rotation is not a valid direction for a Wave.')

        if isinstance(direction, Rotation) and distance not in (90, 180):
            raise ValueError('Rotation distance must be either 90 or 180 degrees.')

    def __str__(self) -> str:
        return self.piece.id + self.direction.shorthand(self.distance)


class Solution:
    def __init__(self, moves: List[Move]):
        self.moves = moves

    def __str__(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(str(move) for move in self.moves)


def find_solution(moves: List[Move]) -> Solution:
    return Solution(moves)
