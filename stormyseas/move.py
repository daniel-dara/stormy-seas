from __future__ import annotations


from stormyseas.directions import Direction


class Move:
    def __init__(self, piece_id: str, direction: Direction, distance: int = 1):
        self.piece_id = piece_id
        self.direction = direction
        self.distance = distance

    def __str__(self) -> str:
        # PyCharm bug (PY-16622)
        # noinspection PyTypeChecker
        return self.piece_id + self.direction.value + str(self.distance)

    def __repr__(self) -> str:
        return self.__str__()

    def can_merge_with(self, other: Move) -> bool:
        return self.piece_id == other.piece_id and self.direction == other.direction

    def merge(self, other: Move) -> None:
        if not self.can_merge_with(other):
            raise ValueError('Cannot combine moves that are different.')

        self.distance += other.distance
