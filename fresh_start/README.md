# Open Considerations

* Instead of calling a validation method for direction in Move, consider having Piece.AllowedDirections which can also be used for enumerating possible moves during puzzle solving.
* Consolidate moves for the same piece in the same direction (summing distance)
* Will Rotation.COUNTER_CLOCKWISE need a Rotation.CLOCKWISE to undo it? Or will 180/270 degree rotations work?
