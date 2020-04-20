from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import List


class Piece:
    def __init__(self, id_: str):
        self.id = id_

    def id(self) -> str:
        return self.id


class Wave(Piece):
    pass


class Boat(Piece):
    pass


class Direction:
    class Type:
        Cardinal = Cardinal
        Rotation = Rotation

    def __init__(self, type_: Type):
        self.type = type_

    @abstractmethod
    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance using Solution Notation."""


class Cardinal(Direction, Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def shorthand(self, distance: int) -> str:
        """Returns a single character representation of the current direction and appends the given distance."""
        return self.value + str(distance)


class Rotation(Direction, Enum):
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1

    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance."""
        return '@@' if distance == 180 else '@'


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self.piece = piece
        self.direction = direction
        self.distance = distance

        if direction.type == Rotation and distance not in (90, 180):
            raise ValueError('Rotational distance must be either 90 or 180 degrees.')

    def __str__(self) -> str:
        return self.piece.id + self.direction.shorthand(self.distance)


class Solution:
    def __init__(self, moves: List[Move]):
        self.moves = moves

    def print(self):
        """Print the solution's moves using Solution Notation."""
        for move in self.moves:
            print(str(move))


def find_solution() -> Solution:
    return Solution([])
