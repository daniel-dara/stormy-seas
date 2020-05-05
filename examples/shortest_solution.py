from stormyseas.solve import Puzzle

input_ = open('../tests/input/problem_2.txt').read()
solution = Puzzle(input_).solve()

print('Solution has %d steps and %d moves.' % (solution.step_count(), solution.move_count()))
print(solution)
