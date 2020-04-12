

def can_boat_move():
    # The boat must not move off the board.
    if boat.is_at_boundary(up|down):
        return False

    # The boat must not move into another boat.
    # for each boat2:
    if boat != boat2:
        if boat.will_hit(up|down, boat2):
            return False

    any(boat.will_hit(direction, boat2) for boat2 in boats)

    # The boat must not move into a blocking wave.
    if not waves[boat.get_top_row()].is_empty_at(boat.get_column):
        return False
