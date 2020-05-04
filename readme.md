# stormyseas

## About the package
`stormyseas` is a Python package for solving challenges for the puzzle game [Stormy Seas](http://www.geekyhobbies.com/stormy-seas-seafaring-puzzle-game-review-puzzled/) (also known as Wave Breaker).

## About the game
[Stormy Seas](http://www.geekyhobbies.com/stormy-seas-seafaring-puzzle-game-review-puzzled/) is a sliding block puzzle game released in 1997 by Binary Arts (now known as [ThinkFun](https://en.wikipedia.org/wiki/ThinkFun)). The game was created by [nob yoshigahara](https://en.wikipedia.org/wiki/Nob_Yoshigahara), author of the more famous game [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)).

Stormy seas is played by sliding pieces around the game board to get the red boat into port (a special space at the bottom of the board).

Setup consists of selecting a challenge card and arranging wave and boat pieces as stated on the card. Then the pieces can be moved around the board by sliding them in various directions. Pieces will block each other so careful moves are required to create a path for the red boat to reach the port.

The game was rebranded in 2016 and renamed to Wave Breaker, for which the instructions are available [here](https://www.thinkfun.com/wp-content/uploads/2016/10/ALLWave-6602-Instructions.pdf).

## Example Usage
View the files in the [examples](examples) directory to see an example of the usage and output of the `Puzzle` class.

`Puzzle` can be constructed from a string representation of any challenge.

The `solve()` method will make valid moves until either a `Solution` is found or it is determined a solution is not possible. If found, a `Solution` is returned which contains the shortest path to solve the puzzle.

## Puzzle Cards
Below are a few cards from the actual game to help visualize puzzle input.
* [Problem 1](https://user-images.githubusercontent.com/1920621/80294652-ca4a3280-8738-11ea-9fda-6aa1ea3460f6.jpg)
  * Solution has 15 steps, 30 moves
* [Problem 2](https://user-images.githubusercontent.com/1920621/80294654-cc13f600-8738-11ea-9160-b67fae22b393.jpg)
  * Solution has 8 steps, 19 moves
* [Problem 3](https://user-images.githubusercontent.com/1920621/80294655-ccac8c80-8738-11ea-80eb-d5895066de72.jpg)
  * Solution has 30 steps, 53 moves

## Puzzle Input
The `Puzzle` class can be initialized with an input string like below.
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

## TODO
* Organize classes into files
* Implement Rotation
* Attempt to find the shortest solution in steps (merged moves)

## Possible future improvements
* Support boat rotation (original puzzle requirement)
* Add animation for puzzle solution
* Add GUI for navigating solution
* GUI for entire puzzle

