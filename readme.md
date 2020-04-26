# Stormy Seas
[Stormy Seas](http://www.geekyhobbies.com/stormy-seas-seafaring-puzzle-game-review-puzzled/) is a sliding block puzzle game released in 1997 by Binary Arts. The game is similar to the more well-known [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)). The objective of Stormy Seas is to slide the red boat to the pocket at the bottom of the board. This requires manipulating the board by sliding the waves horizontally, creating spaces so that the boats themselves can be moved around until the objective is reached.

This repo is an attempt at writing an auto-solver for the puzzle by using depth-first search to exhaustively explore the state space.

# Puzzle examples
* [problem_1](https://user-images.githubusercontent.com/1920621/80294615-b4d50880-8738-11ea-8cc4-894ac76a2f74.jpg)
* [solution_1](https://user-images.githubusercontent.com/1920621/80294652-ca4a3280-8738-11ea-9fda-6aa1ea3460f6.jpg)
* [solution_2](https://user-images.githubusercontent.com/1920621/80294654-cc13f600-8738-11ea-9160-b67fae22b393.jpg)
* [solution_3](https://user-images.githubusercontent.com/1920621/80294655-ccac8c80-8738-11ea-80eb-d5895066de72.jpg)

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

# Algorithm

The algorithm for solving the puzzle is brute force, which means every possible move is tried until the puzzle is solved.

The difficulty is programming the logic to determine which moves are possible. However rather than writing logic that determines if a move *will be* legal, it ends up being simpler to implement logic that makes the move and then determines if it *was* legal.

This only works due to a few interesting properties of the board state. Think of the board as a matrix or a grid. Each cell in the grid represents an empty space, a blocked wave space, or part of a boat.
 
Statement 1:
> Given an initial state, any valid move will result in a new state that still has the same total number of empty cells, blocked cells, and boat cells as the first state.
 
 This can be extended any number of moves to deduce that given an initial state, any number of valid moves will still result in a state with cell counts matching the initial state.
 
 Note that the inverse of this is not true.
 
 Statement 2:
 > Given state A, if the total number of cells (of each type) matches state B, it may or may not be possible to get from A to B with only valid moves.

For example, a set of boats could be deadlocked in state A, such that it is impossible to move. But in state B the same boats could be in a different configuration that allows for them to move. The cell counts would still match but it would be impossible to find valid moves to get from one state to the other.
 
 So how is this useful? So long as moves are executed by the program in a certain way, even invalid moves, the first statement will allow for quick and easy validation of the resulting state.
 
 The rules for moving become:
 * When a boat moves, it overwrites any cell it moves into with itself and overwrites any cell it moves out of with an empty space.
 * When a wave moves, if there are no boats in it the move is always legal
   * If there are any boats, the set of dependent waves must be recursively gathered by finding all the waves touching that boat, and then repeating the process for any other boats that are touching those waves.
   * The set of dependent waves are then all moved together

```python
def get_dependent_boats():
    wave = '---#--0---#1--#-4'
    direction = 1 # Move waves right
    boats = []

    for i in range(len(wave)):
        if wave[i].isdigit() and wave[i - direction] == '#':
            boats.append(wave[i])
```
