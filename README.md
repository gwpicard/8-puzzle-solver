# 8-Puzzle AI Solver

An AI solver for the 8-puzzle game, generalised to n-dimensions of the puzzle.

---

1. [Quickstart](#quickstart)
2. [Files](#files)
3. [Licensing](#licensing)

## Quickstart <a name="quickstart"></a>

**Try the app**

To run the app and solve a puzzle board, run the following pieces of code in sequence.

**Run tests**

To run tests, enter the following into terminal while in the home directory.

`python3 -m unittest discover tests`

## Files <a name="files"></a>

The `8_puzzle_solver.ipynb` notebook contains all of the raw code for the AI puzzle solver, as well as some experiments with different heuristic functions.

`solver.py` contains the functions used to solve the puzzle including the A* search protocol, and the different heuristic functions.

`puzzle.py` contains the puzzle class which defines the puzzle object and the different attributes and method to move the puzzle and keep track of the puzzle state.

`tests.py` contains the unit tests to check all of the functions work as expected.

`main.py` is the main program that can be used to solve a puzzle.

## Licensing<a name="licensing"></a>

[LICENSE information](https://github.com/gwpicard/8-puzzle-solver/blob/master/LICENSE)
