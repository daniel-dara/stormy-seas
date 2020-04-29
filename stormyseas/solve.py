from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections import deque, defaultdict
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Tuple, Union, Set


class Position:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def __str__(self) -> str:
        return '(' + str(self.row) + ', ' + str(self.column) + ')'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.column == other.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))


class Direction(Enum):
    def row_delta(self) -> int:
        pass

    def column_delta(self) -> int:
        pass


class Cardinal(Direction):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def row_delta(self) -> int:
        return self._deltas()[self].row

    def column_delta(self) -> int:
        return self._deltas()[self].column

    @staticmethod
    def _deltas() -> Dict[Direction, Position]:
        return {
            Cardinal.LEFT: Position(0, -1),
            Cardinal.RIGHT: Position(0, 1),
            Cardinal.UP: Position(-1, 0),
            Cardinal.DOWN: Position(1, 0),
        }


class Rotation(Direction):
    # Rotations are only allowed by the 2-square boat in 2x2 channels. Thus only one rotational direction is needed
    # since combined with the use of cardinal directions, the same final positions can be achieved.
    COUNTER_CLOCKWISE = 0


class Piece(ABC):
    def __init__(self, id_: Union[str, int]):
        self.id = id_

    @abstractmethod
    def directions(self) -> Tuple[Direction, ...]:
        """Return a list of directions that this piece is allowed to move. (independent of board state)"""
        pass

    @abstractmethod
    def move(self, direction: Direction) -> None:
        pass

    @abstractmethod
    def positions(self) -> Set[Position]:
        pass

    def collides(self, piece: Piece) -> bool:
        return len(self.positions().intersection(piece.positions())) > 0

    def __str__(self) -> str:
        return '{' + str(self.id) + ': ' + ', '.join(str(position) for position in self.positions()) + '}'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class Boat(Piece):
    def __init__(self, id_: str, positions: Set[Position]):
        super().__init__(id_)
        self._positions = positions

    def directions(self) -> Tuple[Direction, ...]:
        # noinspection PyTypeChecker
        return tuple(Cardinal) + tuple(Rotation) if self.id == Puzzle.RED_BOAT_ID else ()

    def move(self, direction: Direction) -> None:
        if direction == Rotation.COUNTER_CLOCKWISE:
            # TODO implement boat rotation
            pass
        else:
            self._positions = set(
                Position(position.row + direction.row_delta(), position.column + direction.column_delta())
                for position in self._positions
            )

    def is_straight(self) -> bool:
        some_position = next(iter(self._positions))

        return (
                all(some_position.row == position.row for position in self._positions) or
                all(some_position.column == position.column for position in self._positions)
        )

    def positions(self) -> Set[Position]:
        return self._positions


class Wave(Piece):
    def __init__(self, id_: int, bumps: Set[Position]):
        super().__init__(id_)
        self._bumps = bumps

    def directions(self) -> Tuple[Direction, ...]:
        return Cardinal.LEFT, Cardinal.RIGHT

    def move(self, direction: Direction) -> None:
        if direction not in self.directions():
            raise ValueError('Invalid move direction for Wave: ' + direction.name)

        self._bumps = set(
            Position(position.row + direction.row_delta(), position.column + direction.column_delta())
            for position in self._bumps
        )

    def positions(self) -> Set[Position]:
        return self._bumps


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int = 1):
        self._piece = piece
        self._direction = direction
        self._distance = distance

    def __str__(self) -> str:
        # noinspection PyTypeChecker
        return str(self._piece.id) + self._direction.value + str(self._distance)

    def __repr__(self) -> str:
        return self.__str__()


class Solution:
    def __init__(self, moves: List[Move]):
        self._moves = moves

    def __str__(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(str(move) for move in self._moves)

    def length(self) -> int:
        return len(self._moves)


class State:
    """Stores state information about the pieces on the board and manages execution of moves."""

    def __init__(self, boats: Tuple[Boat], waves: Tuple[Wave]):
        self._boats = boats
        self._waves = waves

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish."""
        red_boat = next(boat for boat in self._boats if boat.id == Puzzle.RED_BOAT_ID)
        return red_boat.positions() == Puzzle.FINISH_POSITIONS

    def pieces(self) -> Tuple[Piece]:
        """Returns a list of all the pieces."""
        # noinspection PyTypeChecker
        return self._boats + self._waves

    def move(self, piece: Piece, direction: Direction) -> State:
        """Moves the given piece in the given direction and returns a new state."""
        new_state = deepcopy(self)
        new_piece = new_state.find_piece(piece.id)
        new_state._move(new_piece, direction)
        return new_state

    def _move(self, piece: Piece, direction: Direction) -> None:
        """Same as move() but modifies the current state instance."""
        # TODO: Optimize state generation by caching pushes.
        if isinstance(piece, Wave):
            wave: Wave = piece
            self._push_piece(wave, direction, set())
        elif isinstance(piece, Boat):
            boat: Boat = piece

            if direction in (Cardinal.UP, Cardinal.DOWN):
                boat.move(direction)
            else:
                self._push_piece(boat, direction, set())

    def _push_piece(self, piece: Piece, direction: Direction, pushed_pieces: Set[Piece]) -> Set[Piece]:
        piece.move(direction)
        pushed_pieces.add(piece)

        if isinstance(piece, Wave):
            for boat in self._boats:
                if piece.collides(boat):
                    pushed_pieces |= self._push_piece(boat, direction, pushed_pieces)
        elif isinstance(piece, Boat):
            for position in piece.positions():
                wave = self._waves[position.row]

                if wave.collides(piece):
                    pushed_pieces |= self._push_piece(wave, direction, pushed_pieces)
        else:
            raise ValueError('Impossible piece, not a wave or boat')

        return pushed_pieces

    def is_valid(self) -> bool:
        return not self._has_collision() and self._has_straight_boats() and not self._out_of_bounds()

    def _has_collision(self) -> bool:
        all_positions = self._all_positions()
        return len(all_positions) != len(set(all_positions))

    def _all_boat_positions(self) -> List[Position]:
        return [position for boat in self._boats for position in boat.positions()]

    def _all_wave_positions(self) -> List[Position]:
        return [position for wave in self._waves for position in wave.positions()]

    def _all_positions(self) -> List[Position]:
        return self._all_boat_positions() + self._all_wave_positions()

    # TODO reevaluate if this is needed
    def _has_straight_boats(self) -> bool:
        return all(boat.is_straight() for boat in self._boats)

    def _out_of_bounds(self) -> bool:
        all_positions = self._all_positions()
        all_rows = [position.row for position in all_positions]
        all_columns = [position.column for position in all_positions]

        return min(all_rows) < 0 or max(all_rows) >= len(self._waves) or min(all_columns) < 0 or max(all_columns) >= 9

    def __str__(self) -> str:
        board = [['-'] * 9 for _ in range(8)]

        for wave in self._waves:
            for position in wave.positions():
                board[position.row][position.column] = '#'

        for boat in self._boats:
            for position in boat.positions():
                board[position.row][position.column] = boat.id

        return '\n'.join(''.join(row) for row in board)

    def find_piece(self, id_: Union[str, int]) -> Piece:
        for wave in self._waves:
            if id_ == wave.id:
                return wave

        for boat in self._boats:
            if id_ == boat.id:
                return boat

        raise ValueError('Unable to find Piece with id: ' + str(id_))


class Puzzle:
    RED_BOAT_ID = 'X'
    FINISH_POSITIONS = {Position(6, 5), Position(7, 5)}

    def __init__(self, input_: str):
        boat_positions: Dict[str, Set[Position]] = defaultdict(lambda: set())
        waves = []

        for row, line in enumerate(input_.strip().split('\n')):
            wave_positions = set()

            for column, character in enumerate(line.strip()):
                if character == '#':
                    wave_positions.add(Position(row, column))
                elif character != '-':
                    boat_positions[character].add(Position(row, column))

            waves.append(Wave(row, wave_positions))

        boats = [Boat(id_, positions) for id_, positions in boat_positions.items()]

        self._initial_state = State(tuple(boats), tuple(waves))
        self._current_state = self._initial_state

    def solve(self) -> Solution:
        start = time.time()
        step_start = time.time()

        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        queue = deque([(self._initial_state, 0)])

        # Map of each visited state to its previous state and the move that produced it.
        states: Dict[str, Union[Tuple[State, Move, int], None]] = {str(self._initial_state): None}

        prev_steps = 0
        prev_states_length = len(states)
        prev_queue_length = len(queue)

        while not self._current_state.is_solved() and len(queue) > 0:
            self._current_state, steps = queue.popleft()

            for piece in self._current_state.pieces():
                for direction in piece.directions():
                    new_state = self._current_state.move(piece, direction)

                    if new_state.is_valid() and str(new_state) not in states:
                        queue.append((new_state, steps + 1))
                        states[str(new_state)] = (self._current_state, Move(piece, direction), steps + 1)

            if steps != prev_steps:
                print(steps, len(states), len(states) - prev_states_length, len(queue), len(queue) - prev_queue_length)
                seconds = time.time() - step_start
                print('Time Elapsed: ' + str(int(seconds // 60)) + 'm ' + str(int(seconds % 60)) + 's')
                step_start = time.time()

                if steps == 10:
                    break

            prev_steps = steps
            prev_states_length = len(states)
            prev_queue_length = len(queue)

        seconds = time.time() - start
        print('Completed!')
        # print('Total Solutions: ' + str(total_solutions))
        print('Time Elapsed: ' + str(int(seconds // 60)) + 'm ' + str(int(seconds % 60)) + 's')
        print('Scanned ' + "{:,}".format(len(states)) + ' states with ' +
              "{:,}".format(len(queue)) + ' left in the queue.')

        # if not self._current_state.is_solved():
        #     raise Exception('Puzzle has no solution.')

        return self._generate_solution(states)

    def _generate_solution(self, states: Dict) -> Solution:
        """Generates the solution (list of moves) while iterating backwards from the final state to the initial state.
        """
        moves: List[Move] = []

        while str(self._current_state) != str(self._initial_state):
            previous_state, previous_move, steps = states[str(self._current_state)]
            moves.insert(0, previous_move)
            self._current_state = previous_state

        return Solution(moves)
