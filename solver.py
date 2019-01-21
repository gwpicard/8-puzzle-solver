import numpy as np
from queue import PriorityQueue
import pickle
from puzzle import PuzzleNode

########################################
# Heuristics
########################################

class heuristic_memoization(dict):
    '''
    Memoization class decorator that feeds pre-computed
    heuristic values if available
    '''
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        state = args[0]
        heuristic_name = self.func.__name__

        # check if dictionary for heuristic exists
        if heuristic_name not in self:
            self[heuristic_name] = {}

        state_key = pickle.dumps(state)
        if state_key in self[heuristic_name]: # check if state is memoized
            h_val = self[heuristic_name][state_key]
        else: # else save to memoization dictionary
            h_val = self.func(state)
            self[heuristic_name][state_key] = h_val

        return h_val

@heuristic_memoization
def h1(state):
    '''
    Heuristic function for number of misplaced tiles
    '''
    # count the number of correctly placed tiles
    n = state.shape[0]
    goal_state = np.array([[int(i*n+j) for j in range(n)] for i in range(n)])
    correct = np.sum(goal_state == np.array(state))

    # return number of incorrectly placed tiles
    return n**2-correct

@heuristic_memoization
def h2(state):
    '''
    Heuristic function for Manhattan distance
    The sum of manhattan distances of all tiles from their
    goal state
    '''
    n = state.shape[0]
    goal_state = np.array([[int(i*n+j) for j in range(n)] for i in range(n)])

    manhattan_distance = 0

    # calculate manhattan distance between every goal state and current state
    for i in np.arange(1, n**2):
        x1, y1 = np.where(goal_state == i)
        x2, y2 = np.where(state == i)

        manhattan_distance += (abs(x2[0]-x1[0]) + abs(y2[0]-y1[0]))

    return manhattan_distance

########################################
# Other functions for solvePuzzle
########################################

def puzzleCheck(n, state):
    '''
    Check input state is valid
    '''
    # convert state to numpy array if list
    if type(state) == list:
        state = np.array(state)

    # check shape is correct and all numbers are represented in state array
    if (state.shape == (n,n)) and (list(set(state.flatten())) == list(np.arange(0, n**2))):
        return True

    return False

def retrieve_solution(explored, goal_state):
    '''
    Retrieves the solution path from the explored dictionary by iterating
    from the goal state to the start state through the puzzleNodes
    '''
    # create solution array starting with goal state
    solution = [(goal_state, None)]
    current_state_key = pickle.dumps(goal_state)

    while True:
        last_move = explored[current_state_key].last_move
        previous_state = explored[current_state_key].parent
        if pickle.dumps(explored[current_state_key].parent) == pickle.dumps(None):
            break
        else:
            solution.append((previous_state, last_move))
            current_state_key = pickle.dumps(explored[current_state_key].parent)

    return len(solution)-1, solution[::-1]

def solvePuzzle(n, state, heuristic, prnt):
    '''
    A* Search function given heuristic
    INPUT:
    n - puzzle dimension
    state - starting puzzle state
    heuristic - the heuristic to use for A* search
    prnt - whether or not to print solution

    OUTPUT:
    steps - number of steps to optimally reach goal
    frontierSize - worst-case frontier size during search
    err - error code
    '''
    # default values for output
    steps = 0
    frontierSize = 0
    err = 0

    # keep track of goal state
    goal_state = np.array([[int(i*n+j) for j in range(n)] for i in range(n)]) # goal state of puzzle

    # initialise frontier
    frontier = PriorityQueue()
    # initialise list of explored node objects
    explored = {}

    # check start state is valid
    if puzzleCheck(n, state)==False:
        return steps, frontierSize, -1

    # initialise starting puzzleNode object
    g = 0
    last_move = None
    parent = None
    start_node = PuzzleNode(heuristic, state, g, last_move, parent)

    # pickle states to use as dict key in explored
    start_state_key = pickle.dumps(start_node.state)

    # add starting node to explored states
    explored[start_state_key] = start_node
    # add first object to frontier
    frontier.put((start_node.cost, start_state_key))

    # loop over frontier while it's not empty
    while not frontier.empty():
        # retrieve and remove state with lowest cost from frontier
        _, current_state_key = frontier.get()

        # retrieve current node state
        current_node = explored[current_state_key]

        # check if goal has been reached
        if np.all(current_node.state == goal_state):
            break

        # get allowable moves from node
        moves = current_node.move_choice()

        # iterate over permissible next moves
        for move in moves:
            # get new state after move
            new_state = current_node.move(move)
            new_state_key = pickle.dumps(new_state)

            # create new node from state
            g = current_node.g + 1
            parent = current_node.state
            new_node = PuzzleNode(heuristic, new_state, g, move, parent)

            # get cost of new state from created node
            new_state_cost = new_node.cost

            # get previous cost if state was already explored
            prev_explored_cost = explored.get(new_state_key).cost if explored.get(new_state_key) is not None else 0

            # check if state hasn't been explored or if the current expansion would be
            # cheaper than when previously expanded
            if new_state_key not in explored.keys() or new_state_cost < prev_explored_cost:
                # if so add/update frontier and explored states
                explored[new_state_key] = new_node
                frontier.put((new_state_cost, new_state_key))

        # update frontier size if larger than previous largest size
        if len(frontier.queue) > frontierSize:
            frontierSize = len(frontier.queue)

    # retrieve solution by backtracking through explored states
    steps, solution = retrieve_solution(explored, goal_state)

    # print out solution if option is set in function
    if prnt == True or prnt == 1:
        print("Solution steps: \n")
        for ind, s in enumerate(solution):
            if s[1] != None:
                print(s[0],"\n")
                print("Move %d: %s\n"%(ind+1, s[1]))
            else:
                print(s[0],"\n")
                print("Solved \n")

        print("Number of steps to reach goal: %d \n"%steps)
        print("Maximum frontier size: %d"%frontierSize)

    return steps, frontierSize, err
