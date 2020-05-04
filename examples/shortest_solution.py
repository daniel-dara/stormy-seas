from stormyseas.solve import Puzzle

input_ = open('../tests/input/problem_2.txt').read()
solution = Puzzle(input_).solve()

print('Solution has %d steps.' % solution.length())
print(solution)
