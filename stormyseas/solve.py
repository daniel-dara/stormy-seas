from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Tuple, Union

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

    def is_straight(self) -> bool:
        some_position = next(iter(self.positions))

        return (
            all(some_position.row == position.row for position in self.positions) or
            all(some_position.column == position.column for position in self.positions)
        )


class Wave(Piece):
    EMPTY = '-'
    BLOCKED = '#'

    def __init__(self, id_: int, state: str):
        super().__init__(id_)
        self.state = state  # string of visible gaps, blocks, and boats

    def directions(self) -> Tuple[Direction, ...]:
        return Cardinal.LEFT, Cardinal.RIGHT

    def move(self, direction: Direction) -> None:
        if direction == Cardinal.LEFT:
            self.state = self.state[1:] + self.EMPTY
        elif direction == Cardinal.RIGHT:
            self.state = self.EMPTY + self.state[:-1]
        else:
            raise ValueError('Invalid move direction for Wave: ' + direction.name)


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self.piece = piece
        self.direction = direction
        self.distance = distance

    def __str__(self) -> str:
        # noinspection PyTypeChecker
        return self.piece.id + self.direction.value + str(self.distance)


class Solution:
    def __init__(self, moves: List[Move]):
        self.moves = moves

    def __str__(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(str(move) for move in self.moves)


class State:
    """Stores state information about the pieces on the board and manages execution of moves."""

    def __init__(self, boats: Tuple[Boat], waves: Tuple[Wave], is_valid: bool = True):
        self.boats = boats
        self.waves = waves
        self.is_valid = is_valid

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish."""
        red_boat = next(boat for boat in self.boats if boat.id == Puzzle.RED_BOAT_ID)
        return red_boat.positions == Puzzle.FINISH_POSITIONS

    def pieces(self) -> Tuple[Piece]:
        """Returns a list of all the pieces."""
        # noinspection PyTypeChecker
        return self.boats + self.waves

    def move(self, piece: Piece, direction: Direction) -> State:
        """Moves the given piece in the given direction and returns a new state."""
        new_state = deepcopy(self)

        if isinstance(piece, Wave):
            for piece in self._find_interlocked_pieces(piece):
                piece.move(direction)
        elif isinstance(piece, Boat):
            boat = piece

            for position in boat.positions:
                self.waves[position.row].clear(position.column)

            boat.move(direction)

            for position in boat.positions:
                self.waves[position.row].fill(position.column, boat.id)

        self._validate(new_state)

        return new_state

    def _find_interlocked_pieces(self, piece: Piece) -> List[Piece]:
        # TODO implement
        #   get boats in wave
        #       get unique boat ids in wave
        #   get waves for boats
        #   get new boats
        #   repeat until no new boats
        pass

    def _validate(self, new_state: State) -> None:
        new_state.is_valid = not new_state._has_same_counts(self) and new_state._has_straight_boats()

    def _has_same_counts(self, other: State) -> bool:
        return self._gap_count() == other._gap_count() and self._filled_count() == other._filled_count()

    def _gap_count(self) -> int:
        return sum(wave.state.count('-') for wave in self.waves)

    def _filled_count(self) -> int:
        return sum([len(wave.state) - wave.state.count('-') for wave in self.waves])

    def _has_straight_boats(self) -> bool:
        return all(boat.is_straight() for boat in self.boats)


class Puzzle:
    RED_BOAT_ID = 'X'
    FINISH_POSITIONS = {(6, 5), (7, 5)}

    def __init__(self):
        # TODO read input
        self.initial_state = State(tuple(), tuple())
        self.current_state = self.initial_state

    def solve(self) -> Solution:
        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        queue = deque([self.initial_state])

        # Map of each visited state to its previous state and the move that produced it.
        states: Dict[State, Union[Tuple[State, Direction], None]] = {self.initial_state: None}

        while not self.current_state.is_solved() and len(queue) > 0:
            self.current_state = queue.pop(0)

            for piece in self.current_state.pieces():
                for direction in piece.directions():
                    new_state = self.current_state.move(piece, direction)

                    if new_state not in states and new_state.is_valid:
                        queue.append(new_state)
                        states[new_state] = (self.current_state, direction)

        if not self.current_state.is_solved():
            raise Exception('Puzzle has no solution.')

        return self._generate_solution(states)

    def _generate_solution(self, states: Dict) -> Solution:
        """Generates the solution (list of moves) while iterating backwards from the final state to the initial state.
        """
        moves = []

        while self.current_state != self.initial_state:
            previous_state, previous_move = states[self.current_state]
            moves.insert(0, previous_move)
            self.current_state = previous_move

        return Solution(moves)
