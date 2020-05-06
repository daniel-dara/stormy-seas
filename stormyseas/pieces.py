from __future__ import annotations
from abc import abstractmethod
from typing import NamedTuple, Tuple

from stormyseas.directions import Direction, Rotation, Cardinal
from stormyseas.position import Position


class Piece(NamedTuple):
    id: str
    positions: Tuple[Position]

    @property
    @abstractmethod
    def directions(self) -> Tuple[Direction, ...]:
        """Return a list of the directions that this piece is allowed to move in. (regardless of board state)"""
        raise NotImplementedError()

    @abstractmethod
    def character(self, position: Position) -> str:
        raise NotImplementedError()

    def move(self, direction: Direction) -> Piece:
        if isinstance(direction, Rotation):
            # test later
            raise ValueError('Rotation not supported yet')

        if direction not in self.directions:
            raise ValueError('Invalid move direction for ' + self.__class__.__name__ + ': ' + direction.name)

        positions = direction.transform(self.positions)

        return self.__class__(self.id, positions)

    def collides_with(self, piece: Piece) -> bool:
        # Optimization: Pieces of the same type can't push each other. Waves can only move parallel to each other and
        # will never collide. Boats can collide but there are no waves with enough room for two adjacent boats to
        # push horizontally.
        return type(self) != type(piece) and len(set(self.positions).intersection(piece.positions)) > 0

    def __str__(self) -> str:
        return '{' + self.id + ': ' + ', '.join(str(position) for position in self.positions) + '}'

    def __repr__(self) -> str:
        return self.__str__()


class Boat(Piece):
    RED_BOAT_ID = 'X'

    @property
    def directions(self) -> Tuple[Direction, ...]:
        # Optimization: The game board is sized such that only 2 length boats will ever have room to rotate.
        # PyCharm bug (PY-26133)
        # noinspection PyTypeChecker
        return tuple(Cardinal)  # + (tuple(Rotation) if len(self.positions) == 2 else ())

    def character(self, position: Position) -> str:
        return self.RED_BOAT_ID.lower() if self.id == self.RED_BOAT_ID and self.positions[0] == position else self.id


class Wave(Piece):
    GAP = '-'
    BLOCK = '#'

    @property
    def directions(self) -> Tuple[Direction, ...]:
        return Cardinal.LEFT, Cardinal.RIGHT

    def character(self, position: Position) -> str:
        return self.BLOCK
