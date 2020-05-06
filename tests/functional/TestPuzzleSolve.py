from stormyseas import Puzzle

from tests.utilities import read_test_file, StormySeasTest


class TestPuzzleSolve(StormySeasTest):
    def test_problem_2(self):
        solution = Puzzle(read_test_file('problem_2.txt')).solve()
        self.assertSolutionEqual('4L2, 5L2, XU3, XR2, 6L2, 7L1, 8R2, XD5', solution)
