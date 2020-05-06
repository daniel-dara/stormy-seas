from stormyseas import Puzzle

puzzle_string = open('puzzle.txt').read()
solution = Puzzle(puzzle_string).solve()

print('Solution has %d steps and %d moves.' % (solution.step_count(), solution.move_count()))
print(solution)
