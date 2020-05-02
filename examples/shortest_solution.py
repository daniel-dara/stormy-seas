from stormyseas.solve import Puzzle

input_ = open('../tests/input/problem_2.txt').read()
solution = Puzzle(input_).shortest_solution()

print('Solution has %d moves.' % solution.length())
print(solution.notation())

