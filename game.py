import random
import time
from flow_free_problems import *
from search import astar
from displays import GuiDisplay


class GameEngine(object):
    """
    Game engine class stores the current game state and controls when to
    get input/draw output
    """

    def __init__(self, width, height, num_of_colors):
        # self.display = GuiDisplay(width, height, title='Intro to AI -- 67842 -- Flow Free')
        # self.inputs = inputs

        self.num_of_colors = num_of_colors
        self.board_w = width
        self.board_h = height
        self.turn_num = 0
        self.passed = [False] * self.num_of_colors
        self.score = 0
        self.board = Board(self.board_w, self.num_of_colors)

    def play_turn(self):
        """
        Play a single round of turns.

        Check for empty moves from the inputs (signalling passes) and ask for 
        new moves if illegal moves are provided.
        """
        self.turn_num += 1
        # print "Starting turn %d" % self.turn_num

        available_moves = self.board.get_legal_moves()
        if not available_moves:
            print("No more available moves")
            return None
        else:
            best_move = random.choice(available_moves)
            self.score += self.board.add_move(best_move)
            return best_move

    def _print_board(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board.state]))
        print("-\t" * self.board_w)

    def play_game(self):
        flag_failed = False
        while not self.board.is_game_complete():
            move = self.play_turn()
            # self.display.draw_board(self.board)
            if move is None:
                flag_failed = True
                break
            print(f"Started: {move.get_starting_point()} --> Finished: {move.get_end_point()}")
            self._print_board()
        print("\n")
        if not flag_failed:
            print("Completed board:\n")
        else:
            print("Failed to complete the board:\n")

        self._print_board()
        return self.score

import signal
def signal_handler(signum, frame):
    raise Exception("Timed out!")

def play_simple_search(problem, search_func, display=True):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(60)  # Ten seconds
    st = time.time()
    flag_win = True
    try:
        back_trace = search_func(problem)
    except Exception as msg:
        flag_win = False
        print("Timed out!")
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', round(elapsed_time, 2), 'seconds')
    if display:
        display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Free Flow AI -- 67842 --')
        board = problem.get_start_state()
        # if problem.__class__ == FlowFreeProblem:
        #     dots = [v[0] for k, v in board.all_colors.items()] + [v[1] for k, v in board.all_colors.items()]
        # else:
        #     try:
        #         dots = problem.targets
        #     except AttributeError:
        #         dots = []
        for action in back_trace:
            board.add_move(action)
            # display.draw_board(board, dots=dots)
            display.draw_board(board)
            time.sleep(1)
    # print(f"Expanded nodes: {problem.expanded}, score: {board.scores}")
    print(f"Expanded nodes: {problem.expanded}")
    return [elapsed_time, problem.expanded, flag_win]

#
#
def play_a_star_search(problem, heuristic, display=True):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(60)  # Ten seconds
    st = time.time()
    flag_win = True
    try:
        back_trace = astar(problem, heuristic)
    except Exception as msg:
        flag_win = False
        print("Timed out!")
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', round(elapsed_time, 2), 'seconds')
    if display:
        display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Intro to AI -- 67842 -- FlowFree')
        board = problem.get_start_state()
        if problem.__class__ == FlowFreeProblem:
            dots = [tup for sublist in [v.get_edges() for k, v in board.all_colors.items()] for tup in sublist]
        else:
            try:
                dots = problem.targets
            except AttributeError:
                dots = []
        for action in back_trace:
            board.add_move(action)
            display.draw_board(board, dots=dots)
            # display.draw_board(board)
            time.sleep(0.5)
    # print(f"Expanded nodes: {problem.expanded}, score: {board.scores}")
    print(f"Expanded nodes: {problem.expanded}")
    return [elapsed_time, problem.expanded, flag_win]

#
#
# def play_approximate_search(problem):
#     back_trace = problem.solve()
#     display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Intro to AI -- 67842 -- Ex1')
#     board = problem.get_start_state()
#     for action in back_trace:
#         board.add_move(0, action)
#         display.draw_board(board, dots=problem.targets)
#     print("Expanded nodes: %d, score: %d" % (problem.expanded, board.score(0)))
#
#
# def load_heuristic(heuristic_name):
#     # Looks through all pythonPath Directories for the right function
#     python_path_str = os.path.expandvars("$PYTHONPATH")
#     if python_path_str.find(';') == -1:
#         python_path_dirs = python_path_str.split(':')
#     else:
#         python_path_dirs = python_path_str.split(';')
#     python_path_dirs.append('.')
#
#     for moduleDir in python_path_dirs:
#         if not os.path.isdir(moduleDir):
#             continue
#         module_names = [f for f in os.listdir(moduleDir) if os.path.isfile(f)]
#         for module_name in module_names:
#             try:
#                 module = __import__(str(module_name[:-3]))
#             except ImportError:
#                 continue
#             if heuristic_name in dir(module):
#                 return getattr(module, heuristic_name)
#     raise Exception('The function ' + heuristic_name + ' was not found.')
#
#
# def main():
#     """
#     Processes the command used to run the game from the command line.
#     """
#     from optparse import OptionParser
#     usage_str = """
#     USAGE:      python game.py <options>
#     EXAMPLES:  (1) python game.py
#                   - starts a game between 4 random agents
#                (2) python game.py -p tiny_set.txt -s 4 7
#                OR  python game.py -s 14 14 -f ucs -z cover [(1, 1), (5, 9), (9, 6)]
#     """
#     parser = OptionParser(usage_str)
#
#     parser.add_option('-p', '--pieces', dest='pieces_file',
#                       help='the file to read for the list of pieces',
#                       default='valid_pieces.txt')
#     parser.add_option('-s', '--board-size', dest='size',
#                       type='int', nargs=2, help='the size of the game board.', default=(20, 20))
#     parser.add_option('-f', '--search-function', dest='search_func',
#                       metavar='FUNC',
#                       help='search function to use. This option is ignored for sub-optimal search. ',
#                       type='choice',
#                       choices=['dfs', 'bfs', 'ucs', 'astar'], default='dfs')
#     parser.add_option('-H', '--heuristic', dest='h_func',
#                       help='heuristic function to use for A* search. \
#                       This option is ignored for other search functions. ',
#                       metavar='FUNC', default=None)
#     parser.add_option('-z', '--puzzle', dest='puzzle',
#                       help='the type of puzzle being solved', type='choice',
#                       choices=['fill', 'diagonal', 'corners', 'cover', 'sub-optimal', 'mini-contest'],
#                       default=None)
#     parser.add_option('-x', '--start-point', dest='start', type='int', nargs=2,
#                       help='starting point', default=(0, 0))
#
#     options, cover_points = parser.parse_args()
#     if (options.puzzle == 'cover' or options.puzzle == 'sub-optimal') and len(cover_points) == 0:
#         raise Exception('cover puzzles require at least one point to cover!')
#
#     if options.puzzle == 'cover' or options.puzzle == 'sub-optimal' or options.puzzle == 'mini-contest':
#         targets = ast.literal_eval(''.join(cover_points))
#
#     piece_list = PieceList(options.pieces_file)
#
#     if options.puzzle is None:
#         inputs = [RandomInput() for _ in range(4)]
#         engine = GameEngine(inputs, options.size[1], options.size[0], piece_list)
#         engine.play_game()
#
#     elif options.puzzle == 'sub-optimal':
#         problem = ClosestLocationSearch(options.size[1], options.size[0], piece_list, options.start, targets)
#         play_approximate_search(problem)
#
#     elif options.puzzle == 'mini-contest':
#         problem = MiniContestSearch(options.size[1], options.size[0], piece_list, options.start, targets)
#         play_approximate_search(problem)
#
#     elif options.search_func in ['dfs', 'bfs', 'ucs', 'astar']:
#         if options.puzzle == 'fill':
#             problem = BlokusFillProblem(options.size[1], options.size[0], piece_list, options.start)
#         elif options.puzzle == 'corners':
#             problem = BlokusCornersProblem(options.size[1], options.size[0], piece_list, options.start)
#         elif options.puzzle == 'cover':
#             problem = BlokusCoverProblem(options.size[1], options.size[0], piece_list, options.start, targets)
#
#         if options.search_func in ['dfs', 'bfs', 'ucs']:
#             search = __import__('search')
#             play_simple_search(problem, getattr(search, options.search_func))
#         elif options.search_func == 'astar':
#             play_a_star_search(problem, load_heuristic(options.h_func))
#     else:
#         raise Exception('unrecognized options')
#
#
# if __name__ == "__main__":
#     main()
#     input("Press Enter to continue...")
