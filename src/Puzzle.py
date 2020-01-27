from typing import List, Dict, Set
from src.Direction import Direction
from src.Wave import Wave
from src.Boat import Boat


class Puzzle:
    # The wave (row) and column that the 0-boat must reach for the puzzle to be solved.
    SOLVE_POSITION = (6, 5)

    # The boat that needs to reach SOLVE_POSITION to solve the puzzle.
    SOLVE_BOAT_ID = 0

    def __init__(self, puzzle_input: str):
        self.waves: List[Wave] = []
        self.boats: Dict[int, Boat] = {}
        self.visited_states: Set[str] = set()

        self.load(puzzle_input)

    def load(self, puzzle_input: str) -> None:
        row: int
        line: str

        # Loop over input.
        for row, line in enumerate(puzzle_input.strip().split('\n')):
            column: int
            boat_string_id: str

            # Parse any boats in this wave.
            for column, boat_string_id in filter(lambda x: x[1].isdigit(), enumerate(line)):
                boat_id = int(boat_string_id)

                if boat_id not in self.boats:
                    # Create the boat if it doesn't exist
                    self.boats[boat_id] = Boat(boat_id, row, column, 1)
                else:
                    # Otherwise increase the length since we found another segment.
                    self.boats[boat_id].length += 1

            # Every wave has two empty spaces (gaps) on each end. However each wave is 2 spaces wider than the board,
            # such that two gaps are always hidden. Two gaps on the same end may be hidden or it may be one gap from
            # each end. Gaps are omitted from the puzzle input to make it more readable. Now the gaps are added back
            # to accurately track the waves.
            missing_front_gaps = line.count('#', 0, 2)
            missing_back_gaps = 2 - missing_front_gaps

            full_line = (missing_front_gaps * Wave.GAP) + line + (missing_back_gaps * Wave.GAP)

            self.waves.append(Wave(list(full_line), offset=missing_front_gaps))

    def is_solved(self) -> bool:
        return self.boats[self.SOLVE_BOAT_ID].get_position() == self.SOLVE_POSITION

    # Returns a unique, human-readable representation of the current state that also works as a hash.
    # The returned string uses the same format as the puzzle input.
    def get_state(self) -> str:
        return '\n'.join(str(wave) for wave in self.waves)

    # TODO: Eventually convert this to solve() and return a PuzzleSolution that contains solution steps.
    def is_solvable(self) -> bool:
        if self.is_solved():
            return True

        if self.get_state() in self.visited_states:
            return False

        print(self.get_state(), '\n')
        self.visited_states.add(self.get_state())

        for boat in self.boats.values():
            for direction in [Direction.UP, Direction.DOWN]:
                if boat.can_move(direction, self.waves):
                    boat.move(direction, self.waves)

                    if self.is_solvable():
                        return True

                    boat.move(direction.opposite(), self.waves)

        # for wave in self.waves:
            # for direction in [LEFT, RIGHT]:
                # if wave.canMove(direction):
                    # wave.move(direction)
                # if solve(waves):
                    # return True
                # wave.move(direction.opposite())

        return False

    # BoatMove
    # construct(direction, boat)
    # is_valid()
    #   return not (
    #       boat.is_at_boundary(direction) or
    #       any(boat.will_hit(direction, boat2) for boat2 in boats) or
    #       waves[boat.get_row(direction)].is_blocked(boat.get_column)
    #   )
    # execute()
    #   boat.move(direction)
    # roll_back()
    #   boat.move(direction.opposite())

    # get_state_hash()
    #   return str([wave.get_offset()) for wave in waves] + [boat.get_top_left() for boat in boats])

    # to_ascii()
    # for wave in waves:
    # board = [list(wave.to_ascii()) for wave in waves]
    # for boat in boats:
    #   for row, col in boat.get_all_coordinates():
    #       board[row][col] = boat.get_id()


    # WaveMove
    # wave
    # direction
    # dependentWaves
    # dependentBoats
    # is_valid()
    #   not wave.is_at_boundary(direction)
    #   repeat
    #       dependentBoats.add(get_connected_boats())
    #       dependentWaves.add(get_connected_waves())
    #   for wave in dependentWave:
    #
    #
    # get_connected_boats()
    #   for each boat:
    #       if boat.contains_row(wave.get_row()) and waves.is_blocked_at(boat.get_column() - direction)
