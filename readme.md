# Stormy Seas
[Stormy Seas](http://www.geekyhobbies.com/stormy-seas-seafaring-puzzle-game-review-puzzled/) is a sliding block puzzle game released in 1997 by Binary Arts. The game is similar to the more well-known [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)). The objective of Stormy Seas is to slide the red boat to the pocket at the bottom of the board. This requires manipulating the board by sliding the waves horizontally, creating spaces so that the boats themselves can be moved around until the objective is reached.

This package provides a `Puzzle` class which takes in a string representation of the initial board state and proceeds to find the shortest path measured by individual moves.

## Puzzle examples
* [Problem 1](https://user-images.githubusercontent.com/1920621/80294652-ca4a3280-8738-11ea-9fda-6aa1ea3460f6.jpg)
  * 30 moves / 15 steps
* [Problem 2](https://user-images.githubusercontent.com/1920621/80294654-cc13f600-8738-11ea-9160-b67fae22b393.jpg)
  * 19 moves / 8 steps
* [Problem 3](https://user-images.githubusercontent.com/1920621/80294655-ccac8c80-8738-11ea-80eb-d5895066de72.jpg)
  * 53 moves / 30 steps

## TODO
* Organize classes into files
* Implement Rotation
* Attempt to find the shortest solution in steps (merged moves)

## Possible future improvements
* Support boat rotation (original puzzle requirement)
* Add animation for puzzle solution
* Add GUI for navigating solution
* GUI for entire puzzle

