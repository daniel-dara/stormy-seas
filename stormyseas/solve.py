from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Tuple, Union, Set

puzzle_input = """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-#-#-#
-##0#--#-
###0#-#--
"""


class Position:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column


class Direction(Enum):
    pass


class Cardinal(Direction):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


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

    @abstractmethod  # TODO: Reconcile with move(), probably only need push() with some tweaking.
    def push(self, direction: Direction) -> Set[Piece]:
        pass


class Boat(Piece):
    def __init__(self, id_: str, position: Position):
        super().__init__(id_)
        self.positions = {position}

    def directions(self) -> Tuple[Direction, ...]:
        # noinspection PyTypeChecker
        return tuple(Cardinal) + tuple(Rotation) if self.id == Puzzle.RED_BOAT_ID else ()

    def move(self, direction: Direction):
        if direction == Rotation.COUNTER_CLOCKWISE:
            # TODO implement boat rotation
            pass
        else:
            deltas: Dict[Direction] = {
                Cardinal.LEFT: (0, -1),
                Cardinal.RIGHT: (0, 1),
                Cardinal.UP: (1, 0),
                Cardinal.DOWN: (-1, 0),
            }

            for position in self.positions:
                position.row += deltas[direction][0]
                position.column += deltas[direction][1]

    def push(self, direction: Direction) -> Set[Piece]:
        pass

    def is_straight(self) -> bool:
        some_position = next(iter(self.positions))

        return (
            all(some_position.row == position.row for position in self.positions) or
            all(some_position.column == position.column for position in self.positions)
        )


class Wave(Piece):
    EMPTY = '-'
    BLOCKED = '#'

    def __init__(self, id_: int, slider: List[str]):
        super().__init__(id_)
        self._slider = slider

    def directions(self) -> Tuple[Direction, ...]:
        return Cardinal.LEFT, Cardinal.RIGHT

    # TODO Prevent boat ids from moving if they are not pushed by a block
    def move(self, direction: Direction) -> None:
        if direction == Cardinal.LEFT:
            self._slider = self._slider[1:] + self.EMPTY
        elif direction == Cardinal.RIGHT:
            self._slider = self.EMPTY + self._slider[:-1]
        else:
            raise ValueError('Invalid move direction for Wave: ' + direction.name)

    def push(self, direction: Direction) -> Set[str]:
        self.move(direction)

        slider = self._slider if direction.Cardinal.RIGHT else self._slider[::-1]
        pushed_ids = set()

        for first, second in zip(slider, slider[1:]):
            if first == self.BLOCKED and self.is_boat(second):
                pushed_ids.add(second)

        return pushed_ids

    def pushed_by(self, direction: Direction) -> Set[str]:
        self.move(direction)

        slider = self._slider if direction.Cardinal.RIGHT else self._slider[::-1]
        pushed_by_ids = set()

        for first, second in zip(slider, slider[1:]):
            if second == self.BLOCKED and self.is_boat(first):
                pushed_by_ids.add(second)

        return pushed_by_ids

    def is_boat(self, character: str):
        return character != self.BLOCKED and character != self.EMPTY

    def clear(self, column: int) -> None:
        if 0 <= column < len(self._slider):
            self._slider[column] = self.EMPTY

    def fill(self, column: int) -> None:
        if 0 <= column < len(self._slider):
            self._slider[column] = self.BLOCKED

    def count_gaps(self) -> int:
        return self._slider.count(self.EMPTY)

    def boat_ids(self) -> Set[str]:
        return set(filter(lambda char: char != self.EMPTY and char != self.BLOCKED, self._slider))


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

    def __init__(self, boats: Tuple[Boat], waves: Tuple[Wave], is_valid: bool = True):
        self._boats = boats
        self._waves = waves
        self.is_valid = is_valid

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish."""
        red_boat = next(boat for boat in self._boats if boat.id == Puzzle.RED_BOAT_ID)
        return red_boat.positions == Puzzle.FINISH_POSITIONS

    def pieces(self) -> Tuple[Piece]:
        """Returns a list of all the pieces."""
        # noinspection PyTypeChecker
        return self._boats + self._waves

    def move(self, piece: Piece, direction: Direction) -> State:
        """Moves the given piece in the given direction and returns a new state."""
        new_state = deepcopy(self)

        if isinstance(piece, Wave):
            wave: Wave = piece

            # TODO: Optimize state generation by skipping pieces that are part of a big push.
            self._push(wave, direction, set())
        elif isinstance(piece, Boat):
            boat: Boat = piece

            for position in boat.positions:
                self._waves[position.row].clear(position.column)

            boat.move(direction)

            for position in boat.positions:
                self._waves[position.row].fill(position.column, boat.id)

        self._validate(new_state)

        return new_state

    def _push_boat(self):
        pass

    def _push_wave(self):
        pass

    # Abstracted Piece version with optimized and simpler recurse logic
    def _push(self, piece: Piece, direction: Direction, pushed_pieces: Set[Piece]) -> Set[Piece]:
        # Prevent pushing a piece twice.
        if piece in pushed_pieces:
            return set()

        new_pieces: Set[Piece] = set()

        # Push the piece.
        if isinstance(piece, Boat):
            for position in piece.positions:
                if piece.id in self._waves[position.row].pushed_by(direction):
                    new_pieces |= self._waves[position.row]

            piece.move(direction)
        else:
            new_pieces = piece.push(direction) - pushed_pieces

        # Add it to the set since it has been pushed.
        pushed_pieces |= piece

        # Continue pushing any new pieces.
        for new_piece in new_pieces:
            pushed_pieces |= self._push(new_piece, direction, pushed_pieces)

        return pushed_pieces

    def _validate(self, new_state: State) -> None:
        new_state.is_valid = not new_state._gap_count() == self._gap_count() and new_state._has_straight_boats()

    def _gap_count(self) -> int:
        return sum(wave.count_gaps() for wave in self._waves)

    # TODO reevaluate if this is needed
    def _has_straight_boats(self) -> bool:
        return all(boat.is_straight() for boat in self._boats)


class Puzzle:
    RED_BOAT_ID = 'X'
    FINISH_POSITIONS = {(6, 5), (7, 5)}

    def __init__(self):
        # TODO read input
        self._initial_state = State(tuple(), tuple())
        self._current_state = self._initial_state

    def solve(self) -> Solution:
        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        queue = deque([self._initial_state])

        # Map of each visited state to its previous state and the move that produced it.
        states: Dict[State, Union[Tuple[State, Direction], None]] = {self._initial_state: None}

        while not self._current_state.is_solved() and len(queue) > 0:
            self._current_state = queue.pop(0)

            for piece in self._current_state.pieces():
                for direction in piece.directions():
                    new_state = self._current_state.move(piece, direction)

                    if new_state not in states and new_state.is_valid:
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
