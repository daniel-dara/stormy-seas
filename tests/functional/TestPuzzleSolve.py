from stormyseas import Puzzle

from tests.utilities import StormySeasTest, InputFile


class TestPuzzleSolve(StormySeasTest):
    def test_card_3(self):
        solution = Puzzle(InputFile.CARD_3.read()).solve()
        self.assertSolutionEqual('4L2, 5L2, XU3, XR2, 6L2, 7L1, 8R2, XD5', solution)
