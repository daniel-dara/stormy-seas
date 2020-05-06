from __future__ import annotations
from typing import NamedTuple


class Delta(NamedTuple):
    row: int
    column: int


class Position(NamedTuple):
    row: int
    column: int

    def __add__(self, other: Delta) -> Position:
        return Position(self.row + other.row, self.column + other.column)

    def __sub__(self, other: Position) -> Delta:
        return Delta(self.row - other.row, self.column - other.column)
