from __future__ import annotations
from collections import deque, defaultdict
from itertools import chain
from typing import NamedTuple, Tuple, Iterable, Dict, List

from stormyseas import board
from stormyseas.directions import Direction, Cardinal, Rotation
from stormyseas.pieces import Piece, Wave, Boat
from stormyseas.position import Position


class State(NamedTuple):
    """Stores state information about the pieces on the board and manages execution of moves."""
    pieces: Tuple[Piece]

    @staticmethod
    def from_string(state_string: str) -> State:
        pieces: Dict[str, Piece] = {}
        boat_positions: Dict[str, List[Position]] = defaultdict(lambda: [])

        for row, line in enumerate(state_string.strip().split('\n')):
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

            # Constraint: Rows are 1-based in solution notation so add 1 to the id.
            pieces[str(row + 1)] = Wave(str(row + 1), tuple(wave_positions))

        for id_, positions in boat_positions.items():
            pieces[id_] = Boat(id_, tuple(positions))

        return State(tuple(pieces.values()))

    def is_valid(self) -> bool:
        return not self.has_collision() and not self.has_piece_out_of_bounds()

    def has_collision(self) -> bool:
        positions_list = list(self.all_positions)
        return len(positions_list) != len(set(positions_list))

    def has_piece_out_of_bounds(self) -> bool:
        all_rows, all_columns = zip(*((position.row, position.column) for position in self.all_positions))
        return (
                min(all_rows) < 0 or max(all_rows) >= board.HEIGHT
                or min(all_columns) < 0 or max(all_columns) >= board.WIDTH
        )

    @property
    def all_positions(self) -> Iterable[Position]:
        return chain.from_iterable(piece.positions for piece in self.pieces)

    def is_solved(self) -> bool:
        """Checks if the red boat has reached the finish position (the port)."""
        return self.find_piece(Boat.RED_BOAT_ID).positions == board.PORT

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
        board_matrix = [[Wave.GAP] * board.WIDTH for _ in range(board.HEIGHT)]

        for piece in self.pieces:
            for position in piece.positions:
                board_matrix[position.row][position.column] = piece.character(position)

        return '\n'.join(''.join(row) for row in board_matrix)
