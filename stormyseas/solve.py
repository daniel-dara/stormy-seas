from __future__ import annotations

from itertools import chain
from time import time
from abc import ABC, abstractmethod
from collections import deque, defaultdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Tuple, Union, Set, Iterable, NamedTuple


class Position(NamedTuple):
    row: int
    column: int
    is_front: bool = False

    def __eq__(self, other: Position) -> bool:
        return self.row == other.row and self.column == other.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))


class Direction(Enum):
    @abstractmethod
    def transform(self, positions: Set[Position]) -> Set[Position]:
        pass


class Cardinal(Direction):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def transform(self, positions: Set[Position]) -> Set[Position]:
        return {
            Position(
                position.row + self.DELTAS[self].row,
                position.column + self.DELTAS[self].column,
                position.is_front
            )
            for position in positions
        }


Cardinal.DELTAS = {
    Cardinal.LEFT: Position(0, -1),
    Cardinal.RIGHT: Position(0, 1),
    Cardinal.UP: Position(-1, 0),
    Cardinal.DOWN: Position(1, 0),
}


# TODO Finish implementing Rotation and how it is handled in Boat.move(), prevent rotating through a piece.
class Rotation(Direction):
    COUNTER_CLOCKWISE = 0

    def transform(self, positions: Set[Position]) -> Set[Position]:
        if len(positions) != 2:
            raise ValueError('Only two length pieces should be rotated. '
                             + 'Attempted to rotate piece of length %d.' % len(positions))

        rows, columns = zip(*positions)
        pivot = Position(min(rows), max(columns))
        anchor = Position(max(rows), min(columns))

        if rows[0] == rows[1]:
            delta = Position(-1, -1)
        else:
            delta = Position(1, -1)

        return {anchor, Position(pivot.row + delta.row, pivot.column + delta.column)}


class Piece(ABC):
    def __init__(self, id_: str, positions: Set[Position]):
        self.id = id_
        self._positions = positions

    @property
    def positions(self) -> Set[Position]:
        return self._positions

    @property
    @abstractmethod
    def directions(self) -> Tuple[Direction, ...]:
        """Return a list of the directions that this piece is allowed to move in. (regardless of board state)"""
        pass

    def move(self, direction: Direction) -> None:
        if isinstance(direction, Rotation):
            # test later
            return

        if direction not in self.directions:
            raise ValueError('Invalid move direction for ' + self.__class__.__name__ + ': ' + direction.name)

        self._positions = direction.transform(self._positions)

    def collides_with(self, piece: Piece) -> bool:
        return len(self.positions.intersection(piece.positions)) > 0

    def __str__(self) -> str:
        return '{' + str(self.id) + ': ' + ', '.join(str(position) for position in self.positions) + '}'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class Boat(Piece):
    RED_BOAT_ID = 'X'

    @property
    def directions(self) -> Tuple[Direction, ...]:
        # Optimization: The game board is sized such that only 2 length boats will ever have room to rotate.
        # noinspection PyTypeChecker
        return tuple(Cardinal) + (tuple(Rotation) if len(self._positions) == 2 else ())


class Wave(Piece):
    LENGTH = 9
    GAP = '-'
    BLOCK = '#'

    @property
    def directions(self) -> Tuple[Direction, ...]:
        return Cardinal.LEFT, Cardinal.RIGHT


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int = 1):
        self._piece = piece
        self._direction = direction
        self._distance = distance

    def notation(self) -> str:
        # noinspection PyTypeChecker
        return self._piece.id + self._direction.value + str(self._distance)

    def __str__(self) -> str:
        # noinspection PyTypeChecker
        return str(self._piece.id) + self._direction.value + str(self._distance)

    def __repr__(self) -> str:
        return self.__str__()


class Solution:
    def __init__(self, moves: List[Move]):
        self._moves = moves

    def notation(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(move.notation() for move in self._moves)

    def length(self) -> int:
        return len(self._moves)


class State:
    """Stores state information about the pieces on the board and manages execution of moves."""

    def __init__(self, boats: Tuple[Boat], waves: Tuple[Wave]):
        self._boats = boats
        self._waves = waves
        self._str_cache = None

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish position (the port)."""
        red_boat = self.find_piece(Boat.RED_BOAT_ID)
        return red_boat.positions == Puzzle.PORT and max(red_boat.positions).is_front

    def pieces(self) -> Iterable[Piece]:
        """Returns an iterable of all the pieces."""
        return chain(self._boats, self._waves)

    def find_piece(self, id_: str) -> Piece:
        return next(piece for piece in chain(self._waves, self._boats) if piece.id == id_)

    def copy(self) -> State:
        boats = tuple(Boat(boat.id, boat.positions) for boat in self._boats)
        waves = tuple(Wave(wave.id, wave.positions) for wave in self._waves)
        return State(boats, waves)

    def move(self, piece: Piece, direction: Direction) -> State:
        """Moves the piece in the direction and returns a new state. Handles moving multiple pieces at a time if they
        push each other.
        """
        new_state = self.copy()
        new_piece = new_state.find_piece(piece.id)
        new_state._move(new_piece, direction)
        return new_state

    def _move(self, piece: Piece, direction: Direction) -> None:
        """Same as move() but modifies the current instance."""
        if direction in (Cardinal.UP, Cardinal.DOWN, Rotation.COUNTER_CLOCKWISE):
            # Optimization: There is no need to push pieces vertically since waves are not capable of vertical movement
            # and a boat pushing a boat is equivalent to moving one boat and then the other.
            piece.move(direction)
        else:
            self._push_piece(piece, direction, set())

    def _push_piece(self, piece: Piece, direction: Direction, pushed_pieces: Set[Piece]) -> Set[Piece]:
        piece.move(direction)
        pushed_pieces.add(piece)

        for other_piece in self.pieces():
            # Optimization: Pieces of the same type can't push each other. Waves are orthogonal and will never collide.
            # Boats can collide but there are no waves with enough room for two adjacent boats to push horizontally.
            if type(piece) != type(other_piece):
                if piece.collides_with(other_piece):
                    pushed_pieces |= self._push_piece(other_piece, direction, pushed_pieces)

        return pushed_pieces

    def is_valid(self) -> bool:
        return not self._has_collision() and not self._out_of_bounds()

    def _has_collision(self) -> bool:
        positions_list = list(self._all_positions())
        return len(positions_list) != len(set(positions_list))

    def _out_of_bounds(self) -> bool:
        all_rows, all_columns = zip(*[(position.row, position.column) for position in self._all_positions()])
        return (
            min(all_rows) < 0 or max(all_rows) >= len(self._waves)
            or min(all_columns) < 0 or max(all_columns) >= Wave.LENGTH
        )

    def _all_positions(self) -> Iterable[Position]:
        return chain.from_iterable(piece.positions for piece in self.pieces())

    def __eq__(self, other) -> bool:
        return self.__str__() == other.__str__()

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __str__(self) -> str:
        # TODO Cleanup caching, perhaps make State immutable and put move/push in a new or existing class.
        if self._str_cache is None:
            board = [[Wave.GAP] * Wave.LENGTH for _ in range(len(self._waves))]

            for wave in self._waves:
                for position in wave.positions:
                    board[position.row][position.column] = Wave.BLOCK

            for boat in self._boats:
                for position in boat.positions:
                    board[position.row][position.column] = boat.id.lower() if position.is_front else boat.id

            self._str_cache = '\n'.join(''.join(row) for row in board)

        return self._str_cache


class Puzzle:
    PORT = {Position(6, 5), Position(7, 5)}

    def __init__(self, input_: str):
        self._initial_state = self._Input(input_).parse_state()
        self._current_state = self._initial_state

    def shortest_solution(self) -> Solution:
        return self._solve(self._SearchType.SHORTEST)[0]

    def all_solutions(self) -> List[Solution]:
        return self._solve(self._SearchType.ALL)

    def _solve(self, search_type: _SearchType) -> List[Solution]:
        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        start_time = time()
        step_start = time()

        print('Started solving at: %s' % datetime.fromtimestamp(start_time).strftime('%X'))

        queue = deque([(self._initial_state, 0)])

        # Map of each visited state to its previous state and the move that produced it.
        states: Dict[State, Union[Tuple[State, Move, int], None]] = {self._initial_state: None}

        previous_steps = 0
        previous_states_length = len(states)
        previous_queue_length = len(queue)

        solutions: List[Solution] = []

        while len(queue) > 0 and (search_type == self._SearchType.ALL or not self._current_state.is_solved()):
            self._current_state, steps = queue.popleft()

            if self._current_state.is_solved():
                solutions.append(self._generate_solution(states))
                continue

            for piece in self._current_state.pieces():
                for direction in piece.directions:
                    new_state = self._current_state.move(piece, direction)

                    if new_state.is_valid() and new_state not in states:
                        queue.append((new_state, steps + 1))
                        states[new_state] = (self._current_state, Move(piece, direction), steps + 1)

            if steps != previous_steps:
                seconds = time() - start_time
                step_seconds = time() - step_start
                step_start = time()

                print(
                    'steps=%-2d  states=%-6d%+-5d  queue=%-4d  %+-5d  time=%dm %-3s  %+dm %ds' %
                    (
                        steps,
                        len(states),
                        len(states) - previous_states_length,
                        len(queue),
                        len(queue) - previous_queue_length,
                        seconds // 60,
                        str(round(seconds % 60)) + 's',
                        step_seconds // 60,
                        step_seconds % 60,
                    )
                )

                previous_steps = steps
                previous_states_length = len(states)
                previous_queue_length = len(queue)

        seconds = time() - start_time
        print('Completed! Finished solving at: %s' % datetime.fromtimestamp(time()).strftime('%X'))
        print('Total Solutions: %d' % len(solutions))
        print('Total Time Elapsed: %dm %ds' % (seconds // 60, seconds % 60))
        print('Scanned %s states with %s left in the queue.' % ("{:,}".format(len(states)), "{:,}".format(len(queue))))

        if search_type == self._SearchType.SHORTEST and not self._current_state.is_solved():
            raise Exception('Puzzle has no solution.')

        return solutions

    def _generate_solution(self, states: Dict) -> Solution:
        """Generates the solution (list of moves) while iterating backwards from the final state to the initial state.
        """
        moves = []

        current_state = self._current_state

        while current_state != self._initial_state:
            # TODO find an elegant way to fix the typehints
            previous_state: State
            previous_move: Move
            steps: int

            previous_state, previous_move, steps = states[current_state]
            moves.insert(0, previous_move)
            current_state = previous_state

        return Solution(moves)

    class _SearchType(Enum):
        SHORTEST = 0
        ALL = 1

    class _Input:
        def __init__(self, input_: str):
            self.input = input_

        def parse_state(self) -> State:
            boat_positions: Dict[str, Set[Position]] = defaultdict(lambda: set())
            waves = []

            for row, line in enumerate(self.input.strip().split('\n')):
                wave_positions = set()

                character: str  # Fixes Pycharm Type Inference bug
                for column, character in enumerate(line.strip()):
                    if character == Wave.BLOCK:
                        wave_positions.add(Position(row, column))
                    elif character != Wave.GAP:
                        boat_positions[character.upper()].add(Position(row, column, character.islower()))

                # Constraint: Rows are 1-based in solution notation.
                waves.append(Wave(str(row + 1), wave_positions))

            boats = tuple(Boat(id_, positions) for id_, positions in boat_positions.items())

            return State(boats, tuple(waves))
