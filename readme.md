# stormyseas

## About the package
`stormyseas` is a Python package for solving challenges for the puzzle game [Stormy Seas](http://www.geekyhobbies.com/stormy-seas-seafaring-puzzle-game-review-puzzled/) (also known as [Wave Breaker](https://www.amazon.com/dp/B01MQKC6X7)). It currently requires Python 3.7 or later.

## About the game
_Stormy Seas_ is a puzzle game released in 1997 by Binary Arts. Binary Arts was later renamed to [ThinkFun](https://www.thinkfun.com/press/binary-arts-changes-name-thinkfun/) and the game was re-released as _Wave Breaker_. The game follows similar mechanics to its more famous precursor, [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)).

### Gameplay
Stormy Seas is played by sliding boats and waves around the game board to get the red boat into port (a special space at the bottom of the board).

The game is started by selecting a challenge card and arranging the game pieces as stated on the card. The pieces are then moved around the board by sliding them in various directions. Pieces will block each other so careful planning is required to create a path for the red boat to reach the port.

A PDF of instructions for the re-released Wave Breaker can be found [here](https://www.thinkfun.com/wp-content/uploads/2016/10/ALLWave-6602-Instructions.pdf).

## Examples
View the files in the [examples](examples) directory to see examples of how to specify puzzle input and use the `Puzzle` class to solve a problem.

## Puzzle Cards
Below are a few cards from the actual game to help visualize puzzle input.
* [Problem 1](https://user-images.githubusercontent.com/1920621/80294652-ca4a3280-8738-11ea-9fda-6aa1ea3460f6.jpg) - 15 steps, 30 moves
* [Problem 2](https://user-images.githubusercontent.com/1920621/80294654-cc13f600-8738-11ea-9160-b67fae22b393.jpg) - 8 steps, 19 moves
* [Problem 3](https://user-images.githubusercontent.com/1920621/80294655-ccac8c80-8738-11ea-80eb-d5895066de72.jpg) - 30 steps, 53 moves

## Puzzle Input
The `Puzzle` class can be initialized with an input string of the puzzle state. Here is one example.
```
--#-#X###
#-###x#--
--#H##-##
#-#H###--
#-#H###--
#-###-#--
##-##-#--
--###-###
```
Note the following formatting rules:
* Waves are represented as rows of characters with dashes `-` for gaps and hashes `#` for blocks
* Waves are separated by a single new line `\n`
* Boats are represented by uppercase alphabetical characters `A-Z` and replace gaps `-` in the waves they occupy
  * The red boat, for which the puzzle is being solved, must specifically use the uppercase character `X` for the rear and the lowercase character `x` for the front of the ship.

## Todo
* Test `Rotation.transform`
* Attempt to find the shortest solution in steps (merged moves)

## Ideas
* Add animation for puzzle solution
* Add GUI for navigating solution
* GUI for entire puzzle

