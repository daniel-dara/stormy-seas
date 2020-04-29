from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque, defaultdict
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Tuple, Union, Set


class Position:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column


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
            Cardinal.UP: Position(1, 0),
            Cardinal.DOWN: Position(-1, 0),
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
    def move(self, direction: Direction):
        pass

    @abstractmethod
    def positions(self) -> Set[Position]:
        pass

    def collides(self, piece: Piece) -> bool:
        return len(self.positions().intersection(piece.positions())) > 0


class Boat(Piece):
    def __init__(self, id_: str, positions: Set[Position]):
        super().__init__(id_)
        self._positions = positions

    def directions(self) -> Tuple[Direction, ...]:
        # noinspection PyTypeChecker
        return tuple(Cardinal) + tuple(Rotation) if self.id == Puzzle.RED_BOAT_ID else ()

    def move(self, direction: Direction):
        if direction == Rotation.COUNTER_CLOCKWISE:
            # TODO implement boat rotation
            pass
        else:
            for position in self._positions:
                position.row += direction.row_delta()
                position.column += direction.column_delta()

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

    # TODO Prevent boat ids from moving if they are not pushed by a block
    def move(self, direction: Direction) -> None:
        if direction not in self.directions():
            raise ValueError('Invalid move direction for Wave: ' + direction.name)

        for position in self._bumps:
            position.row += direction.row_delta()
            position.column += direction.column_delta()

    def positions(self) -> Set[Position]:
        return self._bumps


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self._piece = piece
        self._direction = direction
        self._distance = distance

    def __str__(self) -> str:
        # noinspection PyTypeChecker
        return self._piece.id + self._direction.value + str(self._distance)


class Solution:
    def __init__(self, moves: List[Move]):
        self._moves = moves

    def __str__(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(str(move) for move in self._moves)


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
        return deepcopy(self).move(piece, direction)

    def _move(self, piece: Piece, direction: Direction) -> State:
        """Same as move() but modifies the current state instance."""
        # TODO: Optimize state generation by skipping pieces that are part of a big push.
        if isinstance(piece, Wave):
            wave: Wave = piece
            wave.move(direction)
        elif isinstance(piece, Boat):
            boat: Boat = piece
            self._push_piece(boat, direction, set())

        return self

    def _push_piece(self, piece: Piece, direction: Direction, pushed_pieces: Set[Piece]) -> Set[Piece]:
        piece.move(direction)
        pushed_pieces |= piece

        if isinstance(piece, Wave):
            for boat in self._boats:
                if piece.collides(boat):
                    pushed_pieces |= self._push_piece(boat, direction, pushed_pieces)
        elif isinstance(piece, Boat):
            for position in piece.positions():
                wave = self._waves[position.row]

                if wave.collides(piece.positions()):
                    pushed_pieces |= self._push_piece(wave, direction, pushed_pieces)
        else:
            raise ValueError('Impossible piece, not a wave or boat')

        return pushed_pieces

    def is_valid(self) -> bool:
        return not self._has_collision() and self._has_straight_boats()

    def _has_collision(self) -> bool:
        all_positions = self._all_boat_positions() + self._all_wave_positions()
        return len(all_positions) != len(set(all_positions))

    def _all_boat_positions(self) -> List[Position]:
        return [position for boat in self._boats for position in boat.positions()]

    def _all_wave_positions(self) -> List[Position]:
        return [position for wave in self._waves for position in wave.positions()]

    # TODO reevaluate if this is needed
    def _has_straight_boats(self) -> bool:
        return all(boat.is_straight() for boat in self._boats)

    def __str__(self) -> str:
        board = [['-'] * 9 for _ in range(8)]

        for wave in self._waves:
            for position in wave.positions():
                board[position.row][position.column] = '#'

        for boat in self._boats:
            for position in boat.positions():
                board[position.row][position.column] = boat.id

        for row in board:
            row.append('\n')

        return ''.join([char for row in board for char in row])


class Puzzle:
    RED_BOAT_ID = 'X'
    FINISH_POSITIONS = {(6, 5), (7, 5)}

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
        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        queue = deque([self._initial_state])

        # Map of each visited state to its previous state and the move that produced it.
        states: Dict[State, Union[Tuple[State, Direction], None]] = {self._initial_state: None}

        while not self._current_state.is_solved() and len(queue) > 0:
            self._current_state = queue.pop()

            for piece in self._current_state.pieces():
                for direction in piece.directions():
                    new_state = self._current_state.move(piece, direction)

                    if new_state not in states and new_state.is_valid():
                        queue.append(new_state)
                        states[new_state] = (self._current_state, direction)

        if not self._current_state.is_solved():
            raise Exception('Puzzle has no solution.')

        return self._generate_solution(states)

    def _generate_solution(self, states: Dict) -> Solution:
        """Generates the solution (list of moves) while iterating backwards from the final state to the initial state.
        """
        moves = []

        while self._current_state != self._initial_state:
            previous_state, previous_move = states[self._current_state]
            moves.insert(0, previous_move)
            self._current_state = previous_move

        return Solution(moves)
