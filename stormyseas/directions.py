from __future__ import annotations
from abc import abstractmethod
from enum import Enum
from typing import Tuple, Dict

from stormyseas.position import Position, Delta


class Direction(Enum):
    @abstractmethod
    def transform(self, positions: Tuple[Position]) -> Tuple[Position]:
        raise NotImplementedError()

    @abstractmethod
    def opposite(self) -> Direction:
        raise NotImplementedError()


class Cardinal(Direction):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def transform(self, positions: Tuple[Position]) -> Tuple[Position]:
        self.DELTAS: Dict[Cardinal, Delta]  # Defined after class definition.
        return tuple(position + self.DELTAS[self] for position in positions)

    def opposite(self) -> Direction:
        self.OPPOSITES: Dict[Cardinal, Cardinal]  # Defined after class definition.
        return self.OPPOSITES[self]


Cardinal.DELTAS = {
    Cardinal.LEFT: Delta(0, -1),
    Cardinal.RIGHT: Delta(0, 1),
    Cardinal.UP: Delta(-1, 0),
    Cardinal.DOWN: Delta(1, 0),
}

Cardinal.OPPOSITES = {
    Cardinal.LEFT: Cardinal.RIGHT,
    Cardinal.RIGHT: Cardinal.LEFT,
    Cardinal.UP: Cardinal.DOWN,
    Cardinal.DOWN: Cardinal.UP,
}


# TODO Finish implementing Rotation and how it is handled in Boat.move(), prevent rotating through a piece.
class Rotation(Direction):
    COUNTER_CLOCKWISE = 0

    def transform(self, positions: Tuple[Position]) -> Tuple[Position, Position]:
        self.DELTAS: Dict[Rotation, Delta]  # Defined after class definition.

        if len(positions) != 2:
            raise ValueError('Only two length pieces should be rotated. '
                             + 'Attempted to rotate piece of length %d.' % len(positions))

        front = positions[0]
        tail = positions[1] + self.DELTAS[positions[1] - positions[0]]

        return front, tail

    def opposite(self) -> Direction:
        raise NotImplementedError()


Rotation.DELTAS = {
    Delta(1, 0): Delta(-1, 1),
    Delta(0, 1): Delta(-1, -1),
    Delta(-1, 0): Delta(1, -1),
    Delta(0, -1): Delta(1, 1),
}
