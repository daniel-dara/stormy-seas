from stormyseas.solve import Puzzle

input_ = open('../tests/input/problem_1.txt').read()
solutions = Puzzle(input_).all_solutions()

print('Found %d solutions.' % len(solutions))

shortest_solution = min(solutions, key=lambda solution: solution.length())
print('The shortest solution has %d moves.' % shortest_solution.length())
print(shortest_solution.notation())

longest_solution = max(solutions, key=lambda solution: solution.length())
print('The longest solution has %d moves.' % longest_solution.length())
print(longest_solution.notation())
