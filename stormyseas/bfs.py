from __future__ import annotations
from collections import deque
from datetime import datetime
from time import time
from typing import Dict, Optional, List

from stormyseas.pieces import Piece
from stormyseas.move import Move
from stormyseas.state import State


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
