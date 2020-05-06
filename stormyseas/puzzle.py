from __future__ import annotations
from typing import Optional

from stormyseas.bfs import BreadthFirstSearch
from stormyseas.solution import Solution, MoveGenerator
from stormyseas.state import State


class Puzzle:
    """A class for finding solutions to puzzles."""
    DO_MERGE_MOVES = True

    def __init__(self, puzzle_string: str):
        self.initial_state = State.from_string(puzzle_string)
        self.final_state: Optional[State] = None
        self._bfs = BreadthFirstSearch(self.initial_state)

    def solve(self) -> Solution:
        """Finds the shortest set of moves to solve the puzzle using a breadth-first search of all possible states."""
        self.final_state = self._bfs.find_solved_state()
        move_generator = MoveGenerator(self.initial_state, self.final_state, self._bfs.state_map)
        return Solution(move_generator.generate())
