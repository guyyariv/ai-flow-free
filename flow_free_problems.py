from board import Board, get_manhattan_distance
from search import SearchProblem, ucs
import util


class FlowFreeProblem(SearchProblem):
    def __init__(self, board_dimension, num_of_colors, starting_points=None):
        self.expanded = 0
        self.board = Board(board_dimension=board_dimension, num_of_colors=num_of_colors,
                           starting_points=starting_points)
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return state.is_game_complete()

    def get_successors(self, state):
        self.expanded += 1
        return [(state.do_move(move), move, 1) for move in state.get_legal_moves()]

    def get_cost_of_actions(self, actions):
        return actions.board.num_of_colors - len(actions.board.completed_paths_colors)


def flow_free_heuristic(state, problem, dist_function=get_manhattan_distance):
    final_sum = 0
    all_colors = state.all_colors
    for color, color_board in all_colors.items():
        if color in state.completed_paths_colors:
            continue
        edge_1, edge_2 = color_board.get_edges()
        if not color_board.get_color_path():
            final_sum += dist_function(edge_1, edge_2, state.state)
        else:
            color_path = color_board.get_color_path()
            edge_not_in_path = [edge for edge in [edge_1, edge_2] if edge not in color_path][0]
            final_sum += dist_function(color_path[-1], edge_not_in_path, state.state)
    return final_sum

