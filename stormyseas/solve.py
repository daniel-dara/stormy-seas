from __future__ import annotations
from abc import ABC, abstractmethod, ABCMeta
from copy import deepcopy
from enum import Enum, EnumMeta
from typing import List, Dict, Tuple, Set, Type, Union

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
    test = '1'
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

    def validate_direction(self, direction: Direction):
        pass

    @abstractmethod
    def directions(self) -> List[Direction]:
        """Return a list of directions that this piece is allowed to move. (independent of board state)"""
        pass


class Boat(Piece):
    def __init__(self, id_: str, position: Position):
        super().__init__(id_)
        self.positions = {position}

    def directions(self) -> List[Direction]:
        # noinspection PyTypeChecker
        return list(Cardinal) + list(Rotation) if self.id == Puzzle.RED_BOAT_ID else []


class Wave(Piece):
    def __init__(self, id_: int, state: str):
        super().__init__(id_)
        self.state = state  # string of visible gaps, blocks, and boats

    def directions(self) -> List[Direction]:
        return [Cardinal.LEFT, Cardinal.RIGHT]


class Move:
    def __init__(self, piece: Piece, direction: Direction, distance: int):
        self.piece = piece
        self.direction = direction
        self.distance = distance

    def __str__(self) -> str:
        return self.piece.id + self.direction.value

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
    def __init__(self, boats: Tuple[Boat], waves: Tuple[Wave], is_valid: bool = True):
        self.boats = boats
        self.waves = waves
        self.is_valid = is_valid

    def pieces(self) -> Tuple[Piece]:
        # noinspection PyTypeChecker
        return self.boats + self.waves

    def execute(self, move: Move) -> State:
        """Executes the given move and returns the resulting state."""
        new_state = deepcopy(self)

        if isinstance(move.piece, Wave):
            wave = move.piece
            pieces = self.get_interlocked_pieces(wave)
            # TODO reconcile move.piece with piece.execute()...
            [piece.execute(move) for piece in pieces]  # waves are moved and string state changed, boats are only moved
            # wave.execute(): remove character in direction of move, add gap at opposite end
        elif isinstance(move.piece, Boat):
            boat = move.piece

            for position in boat.positions:
                self.waves[position.row].clear(position.column)

            boat.execute(move)

            for position in boat.positions:
                self.waves[position.row].fill(position.column, boat.id)

        # new_state.is_valid == (old gaps, (blocks + boats) == new gaps, (blocks + boats))
        # return new_state


class Puzzle:
    RED_BOAT_ID = 'X'
    FINISH_POSITION = (6, 5)

    def __init__(self, initial_state: str):
        # parse boats (position, orientation, length) or (start x,y end x,y) or (all x,y points)
        self.boats: Dict[str, Boat] = {}

        # parse waves (configuration, position)
        self.waves: List[Wave] = []

        self.current_state = None  # Potential alternative to boats/waves members

        self.initial_gap_count = 0
        self.initial_block_count = 0

    def solve(self) -> Solution:
        """Run a breadth-first search of all possible states until the goal state is reached."""
        moves = []
        queue: List[State] = []  # TODO prepopulate a move
        states = Dict[State, Tuple[State, Move]]  # Maps a state to the previous state and move that led to it.

        while not self.is_solved() and queue != []:
            self.current_state = queue.pop()

            for piece in self.current_state.pieces():
                for direction in piece.directions():
                    new_state = self.current_state.execute(piece, direction)

                    if new_state not in states and new_state.is_valid:
                        queue.append(new_state)
                        states[new_state] = (self.current_state, direction)

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

        # Boat.execute(move)
        #   row_delta = {up: -1, down: 1}  # rest are 0
        #   for block in blocks:
        #       block.row = block.row + row_delta[direction]

        # Boats.is_valid(move)
        #   all locations in bounds
        #   no collisions (same gap, block, boat counts)

        #   all locations +-direction in bounds
        #   no collisions - gap in the space +-direction
        #       gap_at(row, col) -> ()
        #       if direction.up -> min(row)


        # must not hit wave
        # must not hit boat
        #   if states have equal empty/full space counts then it is possible
        pass
