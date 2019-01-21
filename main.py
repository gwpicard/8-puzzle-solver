import argparse
import ast
import numpy as np
from queue import PriorityQueue
import pickle
from puzzle import PuzzleNode
from solver import heuristic_memoization, h2, solvePuzzle

# include arg parser to enable user to use program flexibly
parser = argparse.ArgumentParser()

parser.add_argument('-n','--size', action="store", required=True, dest="n", type=int)
parser.add_argument('-b','--board', nargs='+', action="store", required=True, dest="board")
parser.add_argument('-p','--print', action="store_true", required=False, dest="prnt")

# parse + read arguments
args = parser.parse_args()

n = args.n
board = ast.literal_eval(args.board[0])
prnt = args.prnt

steps, frontierSize, err = solvePuzzle(n, board, h2, prnt)

# print simple solution if print flag not selected
if err == 0 and prnt != True:
    print("No errors")
    print("Numbers of steps to reach goal: %d" % steps)
    print("Maximum frontier size: %d\n" % frontierSize)
elif err != 0:
    print("Error")
