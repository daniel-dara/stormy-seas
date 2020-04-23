from abc import ABC, abstractmethod, ABCMeta
from enum import Enum, EnumMeta
from typing import List


class DirectionMeta(ABCMeta, EnumMeta):
    pass


class Direction(ABC):
    @abstractmethod
    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance using Solution Notation."""
        pass

    def validate_distance(self, distance: int) -> None:
        """Raises a ValueError if the given distance is invalid for the Direction instance."""
        pass


class Cardinal(Direction, Enum, metaclass=DirectionMeta):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def shorthand(self, distance: int) -> str:
        """Returns a single character representation of the current direction and appends the given distance."""
        return self.value + str(distance)


class Rotation(Direction, Enum, metaclass=DirectionMeta):
    # There is no corresponding CLOCKWISE value because Solution Notation uses only the counter-clockwise direction.
    COUNTER_CLOCKWISE = 0

    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance."""
        return '@@' if distance == 180 else '@'

    def validate_distance(self, distance: int) -> None:
        if distance not in (90, 180):
            raise ValueError('Rotation distance must be either 90 or 180 degrees.')


class Piece(ABC):
    def __init__(self, id_: str):
        self.id = id_

    def validate_direction(self, direction: Direction):
        pass


class Wave(Piece):
    def __init__(self, id_: int):
        super().__init__(str(id_))

    def validate_direction(self, direction: Direction):
        if isinstance(direction, Rotation):
            raise ValueError('Rotation is not a valid direction for a Wave.')


class Boat(Piece):
    pass


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self.piece = piece
        self.direction = direction
        self.distance = distance

        piece.validate_direction(direction)
        direction.validate_distance(distance)

    def __str__(self) -> str:
        return self.piece.id + self.direction.shorthand(self.distance)


class Solution:
    def __init__(self, moves: List[Move]):
        self.moves = moves

    def __str__(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(str(move) for move in self.moves)
