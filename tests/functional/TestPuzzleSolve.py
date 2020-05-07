from stormyseas import Puzzle

from tests.utilities import StormySeasTest, Asset


class TestPuzzleSolve(StormySeasTest):
    def test_card_3(self):
        solution = Puzzle(Asset.CARD_3.input).solve()
        self.assertSolutionEqual(Asset.CARD_3.output, solution)

    def test_card_10(self):
        solution = Puzzle(Asset.CARD_10.input).solve()
        self.assertSolutionEqual(Asset.CARD_10.output, solution)

    def test_card_31(self):
        solution = Puzzle(Asset.CARD_31.input).solve()
        self.assertSolutionEqual(Asset.CARD_31.output, solution)
