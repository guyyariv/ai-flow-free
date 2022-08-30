import random
from enum import Enum

import numpy as np

import util


class Colors(Enum):
    NULL_COLOR = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    AQUA = 5
    ORANGE = 6
    PINK = 7
    PURPLE = 8
    BORDO = 9
    WHITE = 10
    BLACK = 11


def get_manhattan_distance(point_1, point_2, state=None):
    return np.sum(np.abs(np.array(point_1) - np.array(point_2)))


def get_maze_distance(point1, point2, gameState):
    copy_state = gameState.copy()
    state = np.where(copy_state != 0, 1, 0)
    state[point1] = 0
    state[point2] = 0
    shortest_path = get_min_distance(state, point1, point2)
    if shortest_path is None:
        return np.inf
    return len(shortest_path)


def get_min_distance(gameState, point1, point2, path=None):
    def try_next(x, y):
        ' Next position we can try '
        return [(a, b) for a, b in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if
                0 <= a < n and 0 <= b < m]

    n = gameState.shape[0]
    m = gameState.shape[1]
    if not path:
        path = [point1]

    # Reached destination
    if point1 == point2:
        return path

    gameState[point1] = 1

    # Recursively find shortest path
    shortest_path = None
    for a, b in try_next(point1[0], point1[1]):
        if not gameState[(a, b)]:
            last_path = get_min_distance(gameState, (a, b), point2,
                                         path + [(a, b)])  # Solution going to a, b next

            if not shortest_path:
                shortest_path = last_path  # Use since haven't found a path yet
            elif last_path and len(last_path) < len(shortest_path):
                shortest_path = last_path  # Use since path is shorter

    gameState[point1] = 0
    return shortest_path


class Board:

    def __init__(self, board_dimension=5, num_of_colors=5, starting_points=None, starting_color=None):
        self.board_w = board_dimension
        self.board_h = board_dimension
        self.num_of_colors = num_of_colors

        self.all_points = starting_points
        board_colors = [m.value for m in Colors][1:][:self.num_of_colors]
        self.all_colors = {color: BoardColor(color, points[0], points[1]) for color, points in
                           zip(board_colors, self.all_points)}
        self.scores = 0
        self.state = np.full((self.board_w, self.board_h), 0, np.int8)
        self.completed_paths_colors = []
        self.current_color = 1
        # if starting_color:
        #     self.current_color = starting_color
        # else:
        #     choose_random = util.flipCoin(0.6)
        #     if choose_random:
        #         self.current_color = random.randint(1, self.num_of_colors)
        #     else:
        #         self.current_color = self.get_min_dist_color()

        for color, board_color in self.all_colors.items():
            edge_1, edge_2 = board_color.get_edges()
            self.state[edge_1] = self.state[edge_2] = color

    def get_min_dist_color(self):
        min_dist = np.inf
        min_color = None
        for color, board_color in self.all_colors.items():
            if color in self.completed_paths_colors:
                continue
            color_edges = list(board_color.get_edges())
            starting_point = color_edges[0]
            end_point = color_edges[1]
            maze_dist = get_manhattan_distance(starting_point, end_point, self.state)
            if maze_dist <= min_dist:
                min_dist = maze_dist
                min_color = color
        return min_color

    def add_move(self, move):
        """
        Try to add <player>'s <move>.

        If the move is legal, the board state is updated; if it's not legal, a
        ValueError is raised.

        Returns the number of tiles placed on the board.
        """
        if not self.check_move_valid(move):
            raise ValueError("Move is not allowed")

        self.state[move.get_end_point()] = move.get_color()

        board_color = self.all_colors[move.get_color()]
        if move.get_starting_point() not in board_color.get_color_path():
            board_color.update_current_path(move.get_starting_point())

        board_color.update_current_path(move.get_end_point())

        if self.color_path_completed(board_color):
            self.completed_paths_colors.append(move.get_color())
            next_color = self.current_color + 1
            self.current_color = next_color if next_color <= self.num_of_colors else self.current_color
            # choose_random = util.flipCoin(0.4)
            # if choose_random:
            #     min_color = random.choice([n for n in range(1, self.num_of_colors + 1) if n not in self.completed_paths_colors])
            # else:
            #     min_color = self.get_min_dist_color()
            # self.current_color = min_color

        return 0

    def do_move(self, move):
        """
        Performs a move, returning a new board
        """
        if move is None:
            return None
        new_board = self.__copy__()
        new_board.add_move(move)

        return new_board

    def get_legal_moves_q(self):
        """
        Returns a list of legal moves for given player for this board state
        """
        # Generate all legal moves
        if self.current_color > self.num_of_colors:
            return None
        move_list = []
        min_board_color = self.all_colors[self.current_color]
        min_edges = min_board_color.get_edges()
        min_color_path = min_board_color.get_color_path()
        start_p = min_edges[0] if not min_color_path else min_color_path[-1]
        x, y = start_p[0], start_p[1]
        options = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for option in options:
            new_move = Move(self.current_color, start_p, option)
            if self.check_move_valid(new_move):
                # move_list.append(new_move)


        # starting_points = list(min_edges) if not min_color_path else [min_color_path[-1]]
        # for start_p in starting_points:
        #     x, y = start_p[0], start_p[1]
        #     options = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        #     for option in options:
        #         new_move = Move(self.current_color, start_p, option)
        #         if self.check_move_valid(new_move):
        #             move_list.append(new_move)
                new_board = self.__copy__()
                next_state = new_board.do_move(new_move)
                if next_state:
                    path_blocked = next_state.check_if_path_blocked()
                    if not path_blocked:
                        move_list.append(new_move)

        return move_list

    #
    # def get_legal_moves_q(self, flag_q=False):
    #     """
    #     Returns a list of legal moves for given player for this board state
    #     """
    #     # Generate all legal moves
    #     move_list = []
    #     q_move_list = []
    #     best_q_move = None
    #     for color, board_color in self.all_colors.items():
    #         min_path_dist = np.inf
    #         color_current_path = board_color.get_color_path()
    #         flag_empty = True if not color_current_path else False
    #         starting_point = list(board_color.get_edges()) if flag_empty else [color_current_path[-1]]
    #         for s in starting_point:
    #             x, y = s[0], s[1]
    #             options = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #             for option in options:
    #                 new_move = Move(color, s, option)
    #                 if self.check_move_valid(new_move):
    #                     move_list.append(new_move)
    #                     if flag_q:
    #                         maze_dist = get_maze_distance(option, [e for e in board_color.get_edges() if e != s][0], self.state)
    #                         # maze_dist = get_manhattan_distance(option, [e for e in board_color.get_edges() if e != s][0], self.state)
    #                         if maze_dist <= min_path_dist:
    #                             min_path_dist = maze_dist
    #                             best_q_move = new_move
    #         if flag_q:
    #             q_move_list.append(best_q_move)
    #     return move_list if not flag_q else q_move_list

    def get_legal_moves(self, flag_q=False):
        if flag_q:
            return self.get_legal_moves_q()
        else:
            return self.get_legal_moves_reg()

    def get_legal_moves_reg(self):
        # Generate all legal moves
        move_list = []
        for color, board_color in self.all_colors.items():
            min_path_dist = np.inf
            color_current_path = board_color.get_color_path()
            flag_empty = True if not color_current_path else False
            starting_point = list(board_color.get_edges()) if flag_empty else [color_current_path[-1]]
            for s in starting_point:
                x, y = s[0], s[1]
                options = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for option in options:
                    new_move = Move(color, s, option)
                    if self.check_move_valid(new_move):
                        move_list.append(new_move)
        return move_list

    def check_move_valid(self, move):
        # Board limits
        if move is None:
            return False
        if not (
                0 <= move.get_starting_point()[0] < self.board_w and 0 <= move.get_end_point()[
            0] < self.board_w and
                0 <= move.get_starting_point()[1] < self.board_h and 0 <= move.get_end_point()[
                    1] < self.board_h):
            return False

        # Color did not finish yet
        if move.get_color() in self.completed_paths_colors:
            return False

        # Distance between start and finish == 1
        if get_manhattan_distance(move.get_starting_point(), move.get_end_point()) != 1:
            return False

        board_color = self.all_colors[move.get_color()]
        # End point of move lands on either 0 or same color as move color
        if move.get_end_point() in board_color.get_color_path():
            return False
        if self.state[move.get_end_point()] != 0 and move.get_end_point() not in board_color.get_edges():
            return False

        # Board color matches the move color
        if self.state[move.get_starting_point()] != move.get_color():
            return False

        # Start move not from the end of path
        color_path = board_color.get_color_path()
        last_moves = board_color.get_edges() if not color_path else [color_path[-1]]
        if move.get_starting_point() not in last_moves:
            return False

        return True

    def check_if_path_blocked(self):
        for color, color_board in self.all_colors.items():
            edges = color_board.get_edges()
            for edge in edges:
                x, y = edge[0], edge[1]
                spots = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                available_spots = []
                for s in spots:
                    if 0 <= s[0] < self.board_w and 0 <= s[1] < self.board_h:
                        available_spots.append(s)
                values = set(self.state[ap[0]][ap[1]] for ap in available_spots)
                if 0 not in values and color not in values:
                    return True
        return False

    def get_position(self, x, y):
        return self.state[x, y]

    def score(self):
        return self.scores

    def __eq__(self, other):
        return np.array_equal(self.state, other.state) and all(
            self.all_colors[color] == other.all_colors[color] for color in list(self.all_colors))

    def __hash__(self):
        return hash(self.__str__())

    # def __str__(self):
    #     out_str = []
    #     for row in range(self.board_h):
    #         for col in range(self.board_w):
    #             if self.state[col, row] == -1:
    #                 out_str.append('_')
    #             else:
    #                 out_str.append(str(self.state[col, row]))
    #         out_str.append('\n')
    #     return ''.join(out_str)

    def __str__(self):
        return str(self.state)

    def __copy__(self):
        cpy_board = Board(board_dimension=self.board_w, num_of_colors=self.num_of_colors,
                          starting_points=self.all_points, starting_color=self.current_color)
        cpy_board.all_points = self.all_points.copy()
        cpy_board.state = np.copy(self.state)
        cpy_board.num_of_colors = self.num_of_colors
        cpy_board.all_colors = {color: color_board.__copy__() for color, color_board in
                                self.all_colors.items()}
        cpy_board.completed_paths_colors = self.completed_paths_colors.copy()
        cpy_board.score = self.score
        cpy_board.current_color = self.current_color
        return cpy_board

    def color_path_completed(self, board_color):
        path = board_color.get_color_path()
        return all([edge in path for edge in board_color.get_edges()])

    def is_game_complete(self):
        if not set(self.completed_paths_colors) == set(list(self.all_colors)):
            return False
        elif 0 in self.state.flatten():
            return False
        else:
            return True


class Move:

    def __init__(self, color, start_point, end_point):
        self.color = color
        self.start = start_point
        self.end = end_point

    def get_color(self):
        return self.color

    def get_starting_point(self):
        return self.start

    def get_end_point(self):
        return self.end

    # def __str__(self):
    #     out_str = [[' ' for _ in range(5)] for _ in range(5)]
    #     for (x, y) in self.orientation:
    #         out_str[x][y] = '0'
    #     out_str = '\n'.join(
    #         [''.join([x_pos for x_pos in out_str[y_val]])
    #          for y_val in range(5)]
    #     )
    #     return ''.join(out_str) + "x: " + str(self.x) + " y: " + str(self.y)

    def __eq__(self, other):
        return self.color == other.color and self.start == other.color and self.end == other.end

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return f"{str(self.color)}-{str(self.start)}-{str(self.end)}"

    def __copy__(self):
        cpy_move = Move(color=self.color, start_point=self.start, end_point=self.end)
        return cpy_move


class BoardColor:

    def __init__(self, color, edge_1, edge_2):
        self.color = color
        self.edge_1 = edge_1
        self.edge_2 = edge_2
        self.current_path = []

    def get_color(self):
        return self.color

    def get_edges(self):
        return self.edge_1, self.edge_2

    def get_color_path(self):
        return self.current_path

    def update_current_path(self, point):
        self.current_path.append(point)

    def __copy__(self):
        cpy_board_color = BoardColor(color=self.color, edge_1=self.edge_1, edge_2=self.edge_2)
        cpy_board_color.current_path = self.current_path.copy()
        return cpy_board_color

    def __eq__(self, other):
        return self.color == other.color and self.edge_1 == other.edge_1 and self.edge_2 == other.edge_2 and self.current_path == other.current_path
