from __future__ import annotations
from abc import ABC, abstractmethod, ABCMeta
from copy import deepcopy
from enum import Enum, EnumMeta
from typing import List, Dict, Tuple, Set

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


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class DirectionMeta(ABCMeta, EnumMeta):
    pass


class Direction(ABC):
    @abstractmethod
    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance using Solution Notation."""
        pass

    def validate_distance(self, distance: int) -> None:
        """Raises a ValueError if the given distance is invalid for the Direction instance."""
        pass


class Cardinal(Direction, Enum, metaclass=DirectionMeta):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def shorthand(self, distance: int) -> str:
        """Returns a single character representation of the current direction and appends the given distance."""
        return self.value + str(distance)


class Rotation(Direction, Enum, metaclass=DirectionMeta):
    # There is no corresponding CLOCKWISE value because Solution Notation uses only the counter-clockwise direction.
    COUNTER_CLOCKWISE = 0

    def shorthand(self, distance: int) -> str:
        """Returns a short string representation of the current direction and given distance."""
        return '@@' if distance == 180 else '@'

    def validate_distance(self, distance: int) -> None:
        if distance not in (90, 180):
            raise ValueError('Rotation distance must be either 90 or 180 degrees.')


class Piece(ABC):
    def __init__(self, id_: str):
        self.id = id_

    def validate_direction(self, direction: Direction):
        pass


class Boat(Piece):
    def __init__(self, id_: str, position: Point2D):
        super().__init__(id_)
        self.positions = {position}


class Wave(Piece):
    def __init__(self, id_: int, state: str):
        super().__init__(str(id_))
        self.state = state  # string of visible gaps, blocks, and boats

    def validate_direction(self, direction: Direction):
        if isinstance(direction, Rotation):
            raise ValueError('Rotation is not a valid direction for a Wave.')


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self.piece = piece
        self.direction = direction
        self.distance = distance

        piece.validate_direction(direction)
        direction.validate_distance(distance)

    def __str__(self) -> str:
        return self.piece.id + self.direction.shorthand(self.distance)

    def execute(self) -> None:
        # Waves
        # move left or right

        # Boats
        # move left/right/up/down or rotate
        pass


class Solution:
    def __init__(self, moves: List[Move]):
        self.moves = moves

    def __str__(self) -> str:
        """Return a string representation of the solution's moves using Solution Notation."""
        return ', '.join(str(move) for move in self.moves)


class State:
    """Serializes state information."""
    def __init__(self, boats: Tuple[Boat], waves: Tuple[Wave]):
        self.boats = boats
        self.waves = waves


class Puzzle:
    RED_BOAT_ID = 'X'
    FINISH_POSITION = (6, 5)

    def __init__(self, initial_state: str):
        # parse boats (position, orientation, length) or (start x,y end x,y) or (all x,y points)
        self.boats: Dict[str, Boat] = {}

        # parse waves (configuration, position)
        self.waves: List[Wave] = []

        self.initial_gap_count = 0
        self.initial_block_count = 0

    def solve(self) -> Solution:
        """Run a breadth-first search of all possible states until the goal state is reached."""
        moves = []
        queue: List[Move] = []  # TODO prepopulate a move
        states = Dict[State, Tuple[State, Move]]  # Maps a state to the previous state and move that led to it.

        while not self.is_solved() and queue != []:
            # TODO implement this
            # pop the next state
            # for each possible move
            #   if new state is not visited and is valid
            #       push state to queue
            #       states[new_state] = [prev_state, move]

            # TODO functionalize rest of this for the above

            # check validity of board state
            #   current gap and block count == initial values

            # generate possible moves
            #   estimated total = 7 waves * 2 directions + 3 boats * 4 directions == 26 moves
            #   for each boat
            #       for each direction (cardinal and rotation)
            #           generate move
            #   for each wave
            #       for each cardinal direction
            #           generate move
            pass

        if not self.is_solved():
            raise Exception('Puzzle has no solution.')

        # try all possible moves until goal is reached
        # don't repeat states

        # solution is the list of moves that reached the goal
        return Solution(moves)

    def is_solved(self) -> bool:
        return self.boats[self.RED_BOAT_ID].position == self.FINISH_POSITION

    def current_state(self) -> Tuple[Tuple[Boat], Tuple[Wave]]:
        return tuple(self.boats.values()), tuple(self.waves)

    # TODO change to Puzzle.is_valid
    def was_last_move_valid(self) -> bool:
        """Compares the current state to the intial state to determine if the last executed move was valid."""
        # Waves - string of empty/full/boat spaces
        # must not hit boundary
        # must not break any boats
        #   get boats in wave
        #       get unique boat ids in wave
        #   get waves for boats
        #   get new boats
        #   repeat until no new boats
        #   can all waves move and not hit boundary
        #   execute move
        #       compare states empty/full space counts
        #       check for broken boats

        # Boats
        # must not hit boundary

        # must not hit wave
        # must not hit boat
        #   if states have equal empty/full space counts then it is possible
        pass
