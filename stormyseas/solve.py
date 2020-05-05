from __future__ import annotations

from itertools import chain
from time import time
from abc import abstractmethod
from collections import deque, defaultdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Tuple, Iterable, NamedTuple, Optional


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


class Direction(Enum):
    @abstractmethod
    def transform(self, positions: Tuple[Position]) -> Tuple[Position]:
        raise NotImplementedError()

    @abstractmethod
    def opposite(self) -> Direction:
        raise NotImplementedError()


class Cardinal(Direction):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def transform(self, positions: Tuple[Position]) -> Tuple[Position]:
        self.DELTAS: Dict[Cardinal, Delta]  # Defined after class definition.
        return tuple(position + self.DELTAS[self] for position in positions)

    def opposite(self) -> Direction:
        self.OPPOSITES: Dict[Cardinal, Cardinal]  # Defined after class definition.
        return self.OPPOSITES[self]


Cardinal.DELTAS = {
    Cardinal.LEFT: Delta(0, -1),
    Cardinal.RIGHT: Delta(0, 1),
    Cardinal.UP: Delta(-1, 0),
    Cardinal.DOWN: Delta(1, 0),
}

Cardinal.OPPOSITES = {
    Cardinal.LEFT: Cardinal.RIGHT,
    Cardinal.RIGHT: Cardinal.LEFT,
    Cardinal.UP: Cardinal.DOWN,
    Cardinal.DOWN: Cardinal.UP,
}


# TODO Finish implementing Rotation and how it is handled in Boat.move(), prevent rotating through a piece.
class Rotation(Direction):
    COUNTER_CLOCKWISE = 0

    def transform(self, positions: Tuple[Position]) -> Tuple[Position, Position]:
        self.DELTAS: Dict[Rotation, Delta]  # Defined after class definition.

        if len(positions) != 2:
            raise ValueError('Only two length pieces should be rotated. '
                             + 'Attempted to rotate piece of length %d.' % len(positions))

        front = positions[0]
        tail = positions[1] + self.DELTAS[positions[1] - positions[0]]

        return front, tail

    def opposite(self) -> Direction:
        raise NotImplementedError()


Rotation.DELTAS = {
    Delta(1, 0): Delta(-1, 1),
    Delta(0, 1): Delta(-1, -1),
    Delta(-1, 0): Delta(1, -1),
    Delta(0, -1): Delta(1, 1),
}


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


class Solution:
    def __init__(self, moves: List[Move]):
        self._moves = moves

    def __str__(self) -> str:
        return ', '.join(str(move) for move in self._moves)

    def step_count(self) -> int:
        """A step is a move of any distance."""
        return len(self._moves)

    def move_count(self) -> int:
        """A move is the act of moving a piece in a direction by one space."""
        return sum(move.distance for move in self._moves)


class State(NamedTuple):
    """Stores state information about the pieces on the board and manages execution of moves."""
    pieces: Tuple[Piece]

    def is_valid(self) -> bool:
        return not self.has_collision() and not self.has_piece_out_of_bounds()

    def has_collision(self) -> bool:
        positions_list = list(self.all_positions)
        return len(positions_list) != len(set(positions_list))

    def has_piece_out_of_bounds(self) -> bool:
        all_rows, all_columns = zip(*((position.row, position.column) for position in self.all_positions))
        return (
            min(all_rows) < 0 or max(all_rows) >= Wave.COUNT
            or min(all_columns) < 0 or max(all_columns) >= Wave.LENGTH
        )

    @property
    def all_positions(self) -> Iterable[Position]:
        return chain.from_iterable(piece.positions for piece in self.pieces)

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish position (the port)."""
        return self.find_piece(Boat.RED_BOAT_ID).positions == Puzzle.PORT

    def find_piece(self, id_: str) -> Piece:
        return next(piece for piece in self.pieces if piece.id == id_)

    def move(self, piece: Piece, direction: Direction) -> State:
        """Moves the piece in the direction and returns a new state. Handles moving multiple pieces at a time if they
        push each other.
        """
        if direction in (Cardinal.UP, Cardinal.DOWN, Rotation.COUNTER_CLOCKWISE):
            # Optimization: There is no need to push pieces vertically since waves are not capable of vertical movement
            # and a boat pushing a boat is equivalent to moving one boat and then the other.
            return State(self._push_without_collision(piece, direction))
        else:
            return State(self._push(piece, direction))

    def undo(self, piece: Piece, direction: Direction) -> State:
        return self.move(piece, direction.opposite())

    def _push_without_collision(self, piece: Piece, direction: Direction) -> Tuple[Piece]:
        old_piece, new_piece = piece, piece.move(direction)
        return tuple(new_piece if piece.id == new_piece.id else piece for piece in self.pieces)

    def _push(self, piece: Piece, direction: Direction) -> Tuple[Piece]:
        pieces = list(self.pieces)
        queue = deque([piece])

        while queue:
            old_piece = queue.popleft()

            new_piece = old_piece.move(direction)
            pieces[pieces.index(old_piece)] = new_piece

            for other_piece in pieces:
                if other_piece not in queue and new_piece.collides_with(other_piece):
                    queue.append(other_piece)

        return tuple(pieces)

    def __str__(self) -> str:
        board = [[Wave.GAP] * Wave.LENGTH for _ in range(Wave.COUNT)]

        for piece in self.pieces:
            for position in piece.positions:
                board[position.row][position.column] = piece.character(position)

        return '\n'.join(''.join(row) for row in board)


class Puzzle:
    PORT = (Position(7, 5), Position(6, 5))
    DO_MERGE_MOVES = True

    def __init__(self, input_: str):
        self.initial_state = PuzzleInput(input_).parse()
        self.final_state: Optional[State] = None
        self._bfs = BreadthFirstSearch(self.initial_state)

    def solve(self) -> Solution:
        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        self.final_state = self._bfs.find_solved_state()
        move_generator = MoveGenerator(self.initial_state, self.final_state, self._bfs.state_map)
        return Solution(move_generator.generate())


class PuzzleInput:
    def __init__(self, input_: str):
        self._input = input_

    def parse(self) -> State:
        boat_positions: Dict[str, List[Position]] = defaultdict(lambda: [])
        pieces: Dict[str, Piece] = {}

        for row, line in enumerate(self._input.strip().split('\n')):
            wave_positions = []

            character: str  # PyCharm bug (PY-42194)
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

        return State(tuple(pieces.values()))


class BreadthFirstSearch:
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.queue = deque([initial_state])
        self.state_map: Dict[State, Optional[Move]] = {initial_state: None}

    def find_solved_state(self) -> State:
        logger = self._Logger(self)
        logger.state_space()

        last_depth_size = len(self.queue)

        while len(self.queue) > 0:
            self.current_state = self.queue.popleft()

            for piece in self.get_ordered_pieces():
                for direction in piece.directions:
                    new_state = self.current_state.move(piece, direction)

                    if new_state.is_valid() and new_state not in self.state_map:
                        self.queue.append(new_state)
                        self.state_map[new_state] = Move(piece.id, direction)

                        if new_state.is_solved():
                            logger.end()
                            return new_state

            last_depth_size -= 1

            if last_depth_size == 0:
                last_depth_size = len(self.queue)
                logger.state_space()

        logger.end()
        raise Exception('Puzzle has no solution.')

    def get_ordered_pieces(self) -> List[Piece]:
        """Orders the pieces so that the piece most recently moved is at the front of the list. This optimizes the
        number of steps in the final solution by increasing the chances of being able to merge moves."""
        pieces = list(self.current_state.pieces)
        last_move = self.state_map[self.current_state]

        if last_move is not None:
            last_moved_piece = self.current_state.find_piece(last_move.piece_id)
            pieces.remove(last_moved_piece)
            pieces.insert(0, last_moved_piece)

        return pieces

    class _Logger:
        def __init__(self, state_search: BreadthFirstSearch):
            self._state_search = state_search
            self._start_time = time()
            self._previous_move_time = self._start_time
            self._previous_states_length = 0
            self._previous_queue_length = 0
            self._depth = 0

            print('Started solving at: %s' % datetime.fromtimestamp(self._start_time).strftime('%X'))

        def state_space(self) -> None:
            total_seconds = time() - self._start_time
            delta_seconds = time() - self._previous_move_time

            print(
                'depth=%-2d  states=%-6d%+-5d  queue=%-4d  %+-5d  time=%dm %-3s  %+dm %ds' %
                (
                    self._depth,
                    len(self._state_search.state_map),
                    len(self._state_search.state_map) - self._previous_states_length,
                    len(self._state_search.queue),
                    len(self._state_search.queue) - self._previous_queue_length,
                    total_seconds // 60,
                    str(round(total_seconds % 60)) + 's',
                    delta_seconds // 60,
                    delta_seconds % 60,
                )
            )

            self._previous_move_time = time()
            self._previous_states_length = len(self._state_search.state_map)
            self._previous_queue_length = len(self._state_search.queue)
            self._depth += 1

        def end(self) -> None:
            seconds = time() - self._start_time
            print('Finished solving at: %s' % datetime.fromtimestamp(time()).strftime('%X'))
            print('Total Time Elapsed: %dm %ds' % (seconds // 60, seconds % 60))
            print('Scanned %s states with %s left in the queue.' %
                  ("{:,}".format(len(self._state_search.state_map)), "{:,}".format(len(self._state_search.queue))))


class MoveGenerator:
    def __init__(self, initial_state: State, final_state: State, state_map: Dict[State, Move]):
        self.initial_state = initial_state
        self.final_state = final_state
        self.state_map = state_map

    def generate(self) -> List[Move]:
        """Generates a list of moves by traversing from the final state to the initial state using the state
        map generated by StateSearch.
        """
        # Every solution will need a final step of XD2 since our Puzzle.PORT position is adjusted to be in bounds.
        moves = [Move(Boat.RED_BOAT_ID, Cardinal.DOWN, 2)]

        current_state = self.final_state

        while current_state != self.initial_state:
            previous_move = self.state_map[current_state]

            if len(moves) > 0 and moves[0].can_merge_with(previous_move):
                moves[0].merge(previous_move)
            else:
                moves.insert(0, previous_move)

            piece = current_state.find_piece(previous_move.piece_id)
            current_state = current_state.undo(piece, previous_move.direction)

        return moves
