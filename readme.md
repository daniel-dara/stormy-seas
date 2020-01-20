# Stormy Seas
[Stormy Seas](http://www.geekyhobbies.com/stormy-seas-seafaring-puzzle-game-review-puzzled/) is a sliding block puzzle game released in 1997 by Binary Arts. The game is similar to the more well-known [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle). The objective of Stormy Seas is to slide the red boat to the pocket at the bottom of the board. This requires manipulating the board by sliding the waves horizontally, creating spaces so that the boats themselves can be moved around until the objective is reached.

This repo is an attempt at writing an auto-solver for the puzzle by using breadth-first search to exhaustively explore the state space.

# Development Notes
## TODO
* Finish coding is_solvable()
    * Finish coding move related methods on Boat and Wave classes
* Convert is_solvable() to solve() and return solution steps

## Future ideas
* Support boat rotation (original puzzle requirement)
* Add animation for puzzle solution
* Add GUI for navigating solution
* GUI for entire puzzle
