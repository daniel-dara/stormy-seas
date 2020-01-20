from typing import Tuple


class Boat:
    def __init__(self, row: int, column: int, length: int):
        self.row = row
        self.column = column
        self.length = length

    def __repr__(self):
        return 'Boat' + str([self.row, self.column, self.length])

    def get_position(self) -> Tuple[int, int]:
        return self.row, self.column

    def can_move(self, direction) -> bool:
        # for up/down
        return False

    def move(self, direction) -> None:
        return
