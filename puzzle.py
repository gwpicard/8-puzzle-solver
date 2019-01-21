import numpy as np

class PuzzleNode():
    '''
    PuzzleNode class for node states and state bookkeeping
    '''
    def __init__(self, heuristic, state, g, last_move, parent):
        # convert state to numpy array if list
        if type(state) == list:
            state = np.array(state)

        self.size = state.shape[0] # node state dimension size
        self.state = state.astype(int)  # set PuzzleNode state
        self.gap_position = [i[0] for i in np.where(self.state == 0)]  # position of gap in node state
        self.g = g # g(n) cost
        self.cost = g + heuristic(self.state) # f(n) = g(n) + h(n)
        self.last_move = last_move # move needed to get to node state
        self.parent = parent # parent state of node state

    def move_choice(self):
        '''
        Return list of allowable moves
        '''
        not_permitted = {'right':'left', 'up':'down', 'left':'right', 'down':'up'}
        possible_moves = set()
        x, y = self.gap_position

        if 0 < x < (self.size-1):
            possible_moves.add("up")
            possible_moves.add("down")
        elif x == 0:
            possible_moves.add("up")
        else:
            possible_moves.add("down")

        if 0 < y < (self.size-1):
            possible_moves.add("left")
            possible_moves.add("right")
        elif y == 0:
            possible_moves.add("left")
        else:
            possible_moves.add("right")

        # remove undo move from allowable moves
        undo_move = set()
        undo_move.add(not_permitted[self.last_move]) if self.last_move is not None else None
        possible_moves = possible_moves - undo_move

        return list(possible_moves)

    def move(self, move):
        '''
        Move puzzle given allowable move
        '''
        # copy puzzle state to prevent corruption
        new_state = self.state.copy()
        x, y = self.gap_position

        # slide left
        if move == "left":
            new_state[x, y] = self.state[x, y+1]
            new_state[x, y+1] = self.state[x, y]
        # slide right
        if move == "right":
            new_state[x, y] = self.state[x, y-1]
            new_state[x, y-1] = self.state[x, y]
        # slide up
        if move == "up":
            new_state[x, y] = self.state[x+1, y]
            new_state[x+1, y] = self.state[x, y]
        # slide down
        if move == "down":
            new_state[x, y] = self.state[x-1, y]
            new_state[x-1, y] = self.state[x, y]

        # return new state after move is made
        return new_state.astype(int)

    def __str__(self):
        '''
        Print out the current puzzle state
        '''
        return str(self.state)
