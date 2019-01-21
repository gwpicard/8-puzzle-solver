import numpy as np
from queue import PriorityQueue
import pickle
import unittest
from puzzle import PuzzleNode
from solver import heuristic_memoization, h1, h2, solvePuzzle

class TestNotebook(unittest.TestCase):
    '''
    Function to test PuzzleNode class
    functionality
    '''
    def test_dimension(self):
        '''
        Check if puzzles of different sizes
        are created correctly
        '''
        dims = []
        for n in [2,3,6,12]:
            state = np.zeros((n,n)).astype(int)
            g = 0
            last_move = None
            parent = None
            node = PuzzleNode(h1, state, g, last_move, parent)
            dims.append((node.state.shape))

        self.assertEqual(dims, [(2,2),(3,3),(6,6),(12,12)])

    def test_gap_position(self):
        '''
        Check if gap position is correct
        for custom state setting
        '''
        state = [[1,1,1],[1,0,1],[1,1,1]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)
        gap_position = node.gap_position

        self.assertEqual(gap_position, [1,1])

    def test_move_choice_one(self):
        '''
        Check if move_choice function works as expected
        '''
        state = [[1,1,1],[1,1,1],[1,1,0]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)

        self.assertEqual(set(node.move_choice()) == set(['right', 'down']), 1)

    def test_move_choice_two(self):
        '''
        Check if move_choice function works as expected
        '''
        state = [[1,0,1],[1,1,1],[1,1,1]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)

        self.assertEqual(set(node.move_choice()) == set(['left', 'right', 'up']), 1)

    def test_move_choice_three(self):
        '''
        Check if move_choice function works as expected
        '''
        state = [[1,0,1],[1,1,1],[1,1,1]]
        g = 0
        last_move = "left"
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)

        self.assertEqual(set(node.move_choice()) == set(['left', 'up']), 1)

    def test_move_left(self):
        '''
        Check if move left function works as expected
        '''
        state = [[1, 0, 2],[3, 4, 5],[6, 7, 8]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)
        new_state = node.move('left')

        expected_new = [[1, 2, 0],[3, 4, 5],[6, 7, 8]]

        self.assertEqual(np.all(new_state == expected_new), 1)

    def test_move_right(self):
        '''
        Check if move right function works as expected
        '''
        state = [[1,1,1],[1,1,1],[1,1,0]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)
        new_state = node.move('right')

        expected_new = [[1,1,1],[1,1,1],[1,0,1]]

        self.assertEqual(np.all(new_state == expected_new), 1)

    def test_move_down(self):
        '''
        Check if move down function works as expected
        '''
        state = [[1,1,1],[1,0,1],[1,1,1]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)
        new_state = node.move('down')

        expected_new = [[1,0,1],[1,1,1],[1,1,1]]

        self.assertEqual(np.all(new_state == expected_new), 1)

    def test_move_up(self):
        '''
        Check if move up function works as expected
        '''
        state = [[1,1,1],[1,0,1],[1,1,1]]
        g = 0
        last_move = None
        parent = None
        node = PuzzleNode(h1, state, g, last_move, parent)
        new_state = node.move('up')

        expected_new = [[1,1,1],[1,1,1],[1,0,1]]

        self.assertEqual(np.all(new_state == expected_new), 1)

    def test_misplaced_tiles_one(self):
        '''
        Check misplaced tiles heuristic works correctly
        '''
        state = np.array([[0,1,2],[3,4,5],[6,7,8]])
        val = h1(state)

        self.assertEqual(val, 0)

    def test_misplaced_tiles_two(self):
        '''
        Check misplaced tiles heuristic works correctly
        '''
        state = np.array([[1,2,0],[4,3,5],[6,8,7]])
        val = h1(state)

        self.assertEqual(val, 7)

    def test_manhattan_distance_one(self):
        '''
        Check manhattan distance heuristic works correctly
        '''
        state = np.array([[0,1,2],[3,4,5],[6,7,8]])
        val = h2(state)

        self.assertEqual(val, 0)

    def test_manhattan_distance_two(self):
        '''
        Check manhattan distance heuristic works correctly
        '''
        state = np.array([[1,0,2],[3,4,5],[6,7,8]])
        val = h2(state)

        self.assertEqual(val, 1)

    def test_manhattan_distance_three(self):
        '''
        Check manhattan distance heuristic works correctly
        '''
        state = np.array([[2,1,0],[3,5,4],[6,8,7]])
        val = h2(state)

        self.assertEqual(val, 6)

    def test_solve_puzzle_one(self):
        '''
        Check incorrect puzzles are not accepted
        '''
        res = solvePuzzle(3, [[0,0,0],[0,0,0],[0,0,0]], h1, 0)

        self.assertEqual(res, (0,0,-1))

    def test_solve_puzzle_two(self):
        '''
        Check incorrect puzzles are not accepted
        '''
        res = solvePuzzle(3, [[0,1,2],[3,4,5],[6,6,8]], h1, 0)

        self.assertEqual(res, (0,0,-1))

    def test_solve_puzzle_three(self):
        '''
        Check incorrect puzzles are not accepted
        '''
        res = solvePuzzle(3, [[1,0,2],[3,4,5],[6,7,8]], h1, 0)

        self.assertEqual(res, (1,3,0))

unittest.main(argv=[''], verbosity=2, exit=False)
