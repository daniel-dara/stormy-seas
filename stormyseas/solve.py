from __future__ import annotations

from itertools import chain
from time import time
from abc import abstractmethod
from collections import deque, defaultdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Tuple, Union, Iterable, NamedTuple, Set, FrozenSet


class Position(NamedTuple):
    row: int
    column: int

    def __sub__(self, other: Position):
        return Position(self.row - other.row, self.column - other.column)


class Direction(Enum):
    @abstractmethod
    def transform(self, positions: Tuple[Position]) -> Tuple[Position]:
        pass


class Cardinal(Direction):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def transform(self, positions: Tuple[Position]) -> Tuple[Position]:
        return tuple(
            Position(
                position.row + self.DELTAS[self].row,
                position.column + self.DELTAS[self].column
            )
            for position in positions
        )


Cardinal.DELTAS = {
    Cardinal.LEFT: Position(0, -1),
    Cardinal.RIGHT: Position(0, 1),
    Cardinal.UP: Position(-1, 0),
    Cardinal.DOWN: Position(1, 0),
}


# TODO Finish implementing Rotation and how it is handled in Boat.move(), prevent rotating through a piece.
class Rotation(Direction):
    COUNTER_CLOCKWISE = 0

    def transform(self, positions: Tuple[Position]) -> Tuple[Position, Position]:
        if len(positions) != 2:
            raise ValueError('Only two length pieces should be rotated. '
                             + 'Attempted to rotate piece of length %d.' % len(positions))

        front = positions[0]
        tail = self.DELTAS[positions[1] - positions[0]]

        return front, tail


Rotation.DELTAS = {
    Position(1, 0): Position(-1, 1),
    Position(0, 1): Position(-1, -1),
    Position(-1, 0): Position(1, -1),
    Position(0, -1): Position(1, 1),
}


class Piece(NamedTuple):
    id: str
    positions: Tuple[Position]

    @property
    @abstractmethod
    def directions(self) -> Tuple[Direction, ...]:
        """Return a list of the directions that this piece is allowed to move in. (regardless of board state)"""
        pass

    @abstractmethod
    def character(self, position: Position) -> str:
        pass

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
        # noinspection PyTypeChecker
        return tuple(Cardinal)  # + (tuple(Rotation) if len(self.positions) == 2 else ())

    def character(self, position: Position) -> str:
        return self.RED_BOAT_ID.lower() if self.id == self.RED_BOAT_ID and self.positions[0] == position else self.id


class Wave(Piece):
    LENGTH = 9
    COUNT = 8
    GAP = '-'
    BLOCK = '#'

    @property
    def directions(self) -> Tuple[Direction, ...]:
        return Cardinal.LEFT, Cardinal.RIGHT

    def character(self, position: Position) -> str:
        return self.BLOCK


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
        return self._piece.id + self._direction.value + str(self._distance)

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


class State(NamedTuple):
    """Stores state information about the pieces on the board and manages execution of moves."""
    pieces: FrozenSet[Piece]

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish position (the port)."""
        return next(piece for piece in self.pieces if piece.id == Boat.RED_BOAT_ID).positions == Puzzle.PORT

    def move(self, piece: Piece, direction: Direction) -> State:
        """Moves the piece in the direction and returns a new state. Handles moving multiple pieces at a time if they
        push each other.
        """
        old_pieces, new_pieces = self._move(piece, direction)
        return State(frozenset((self.pieces - old_pieces) | new_pieces))

    def _move(self, piece: Piece, direction: Direction) -> Tuple[Set[Piece], Set[Piece]]:
        """Same as move() but modifies the current instance."""
        if direction in (Cardinal.UP, Cardinal.DOWN, Rotation.COUNTER_CLOCKWISE):
            # Optimization: There is no need to push pieces vertically since waves are not capable of vertical movement
            # and a boat pushing a boat is equivalent to moving one boat and then the other.
            return {piece}, {piece.move(direction)}
        else:
            return self._push_piece(piece, direction, set(), set())

    # TODO Try using a dictionary of self.pieces and mutating it before making frozenset
    def _push_piece(
        self,
        piece: Piece,
        direction: Direction,
        pushed_pieces: Set[Piece],
        old_pieces: Set[Piece]
    ) -> Tuple[Set[Piece], Set[Piece]]:
        old_pieces.add(piece)
        new_piece = piece.move(direction)

        pushed_pieces.add(new_piece)

        for other_piece in self.pieces - old_pieces:
            if new_piece.collides_with(other_piece):
                self._push_piece(other_piece, direction, pushed_pieces, old_pieces)

        return old_pieces, pushed_pieces

    def is_valid(self) -> bool:
        return not self._has_collision() and not self._out_of_bounds()

    def _has_collision(self) -> bool:
        positions_list = list(self._all_positions())
        return len(positions_list) != len(set(positions_list))

    def _out_of_bounds(self) -> bool:
        all_rows, all_columns = zip(*[(position.row, position.column) for position in self._all_positions()])
        return (
            min(all_rows) < 0 or max(all_rows) >= Wave.COUNT
            or min(all_columns) < 0 or max(all_columns) >= Wave.LENGTH
        )

    def _all_positions(self) -> Iterable[Position]:
        return chain.from_iterable(piece.positions for piece in self.pieces)

    def __str__(self) -> str:
        board = [[Wave.GAP] * Wave.LENGTH for _ in range(Wave.COUNT)]

        for piece in self.pieces:
            for position in piece.positions:
                board[position.row][position.column] = piece.character(position)

        return '\n'.join(''.join(row) for row in board)


class Puzzle:
    PORT = (Position(7, 5), Position(6, 5))

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

            if self._current_state.is_solved():
                solutions.append(self._generate_solution(states))
                continue

            for piece in self._current_state.pieces:
                for direction in piece.directions:
                    new_state = self._current_state.move(piece, direction)

                    if new_state.is_valid() and new_state not in states:
                        queue.append((new_state, steps + 1))
                        states[new_state] = (self._current_state, Move(piece, direction), steps + 1)

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
            boat_positions: Dict[str, List[Position]] = defaultdict(lambda: [])
            pieces: Dict[str, Piece] = {}

            for row, line in enumerate(self.input.strip().split('\n')):
                wave_positions = []

                character: str  # Fixes Pycharm Type Inference bug
                for column, character in enumerate(line.strip()):
                    if character == Wave.BLOCK:
                        wave_positions.append(Position(row, column))
                    elif character != Wave.GAP:
                        if character.islower():
                            # The first position should be the front of the boat.
                            boat_positions[character.upper()].insert(0, Position(row, column))
                        else:
                            boat_positions[character.upper()].append(Position(row, column))

                # Constraint: Rows are 1-based in solution notation.
                pieces[str(row + 1)] = Wave(str(row + 1), tuple(wave_positions))

            for id_, positions in boat_positions.items():
                pieces[id_] = Boat(id_, tuple(positions))

            return State(frozenset(pieces.values()))
