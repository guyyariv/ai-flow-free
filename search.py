"""
In search.py, you will implement generic search algorithms
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class StateAndMoves(object):
    def __init__(self, board, moves):
        self.board = board
        self.moves = moves


def global_search(problem, search_func):
    if problem.is_goal_state(problem.get_start_state()):
        return
    visited_states = set()
    search_func.push(StateAndMoves(problem.get_start_state(), []))
    while not search_func.isEmpty():
        final_path = search_func.pop()
        current_state = final_path.board
        if current_state not in visited_states:
            visited_states.add(current_state)
            child_states = problem.get_successors(current_state)
            for child in child_states:
                search_func.push(StateAndMoves(child[0], final_path.moves + [child[1]]))
                if problem.is_goal_state(child[0]):
                    print('win')
                    return final_path.moves + [child[1]]


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    state_stack = util.Stack()
    return global_search(problem, state_stack)


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    state_queue = util.Queue()
    return global_search(problem, state_queue)


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    state_priority_queue = util.PriorityQueueWithFunction(problem.get_cost_of_actions)
    return global_search(problem, state_priority_queue)


def null_heuristic(state, problem=None, dist_func=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic_tuple=(null_heuristic, None)):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    heuristic = heuristic_tuple[0]
    dist_func = heuristic_tuple[1]
    def heuristic_cost_function(state_and_moves):
        g_func = problem.get_cost_of_actions(state_and_moves)
        h_func = heuristic(state_and_moves.board, problem, dist_func)
        return g_func + h_func

    state_priority_queue = util.PriorityQueueWithFunction(heuristic_cost_function)
    return global_search(problem, state_priority_queue)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
