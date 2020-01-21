from typing import Tuple, List
from src.Board import Board
from src.Direction import Direction
from src.Wave import Wave


class Boat:
    def __init__(self, boat_id: int, row: int, column: int, length: int):
        self.id = boat_id
        self.row = row
        self.column = column
        self.length = length

    def __repr__(self):
        return 'Boat' + str([self.row, self.column, self.length])

    def get_position(self) -> Tuple[int, int]:
        return self.row, self.column

    def can_move(self, direction: Direction, waves: List[Wave]) -> bool:
        if direction == Direction.UP:
            if self.get_top_row() == Board.FIRST_ROW:
                return False

            if not self.get_wave_above(waves).is_empty_at(self.get_column()):
                return False

            return True
        elif direction == Direction.DOWN:
            if self.get_bottom_row() == Board.LAST_ROW:
                return False

            if not self.get_wave_below(waves).is_empty_at(self.get_column()):
                return False

            return True

    def move(self, direction: Direction, waves: List[Wave]) -> None:
        if direction == Direction.UP:
            waves[self.get_bottom_row()][self.column] = Wave.GAP

            # self.get_wave_above(waves)[self.column] = str(self.id)
            self.row -= 1
            # self.get_wave_below(waves)[self.column] = Wave.GAP

            waves[self.get_top_row()][self.column] = str(self.id)
        elif direction == Direction.DOWN:
            waves[self.get_top_row()][self.column] = Wave.GAP
            self.row += 1
            waves[self.get_bottom_row()][self.column] = str(self.id)
        else:
            raise Exception('Invalid argument. direction should either be \'up\' or \'down\'. ' +
                            'direction was: ' + str(direction))

    def get_wave_above(self, waves: List[Wave]):
        return waves[self.get_top_row() - 1]

    def get_wave_below(self,  waves: List[Wave]):
        return waves[self.get_bottom_row() + 1]

    def get_column(self) -> int:
        return self.column

    def get_top_row(self) -> int:
        return self.row

    def get_bottom_row(self) -> int:
        return self.row + self.length - 1
