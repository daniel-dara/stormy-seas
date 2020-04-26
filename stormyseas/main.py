from stormyseas.solve import *

moves = [
     Move(Boat('X'), Rotation.COUNTER_CLOCKWISE, 180),
     Move(Wave(3), Cardinal.UP, 1),
     Move(Boat('Z'), Cardinal.LEFT, 2),
     Move(Boat('X'), Rotation.COUNTER_CLOCKWISE, 90),
]

print(Solution(moves))
