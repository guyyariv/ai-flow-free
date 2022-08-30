import click as click
import boards
import qlearningAgents
from board import get_maze_distance, get_manhattan_distance
from flow_free_problems import flow_free_heuristic
from game import play_simple_search, play_a_star_search
from search import *


@click.command()
@click.option('--a', help='algorithm name', type=str, default='q')
@click.option('--s', help='board size', type=int, default=5)
@click.option('--l', help='easy, medium or hard', default='easy')
def main(a, size, level):


    print('size: ', size, '; level: ', level)
    print()

    if a == 'q':
        board = boards.InitialBoard(size=size, level=level)
        ff_problem = board.get_initial_board()
        print('Approximate Q Learning:')
        qlearningAgents.exactQ(ff_problem.board, 0.5, 0.5, 0.5, 1000)
        print()

    elif a == 'dfs':
        board = boards.InitialBoard(size=size, level=level)
        ff_problem = board.get_initial_board()
        print('DFS:')
        search_func = depth_first_search
        play_simple_search(ff_problem, search_func)
        print()

    elif a == 'bfs':
        board = boards.InitialBoard(size=size, level=level)
        ff_problem = board.get_initial_board()
        print('BFS:')
        search_func = breadth_first_search
        play_simple_search(ff_problem, search_func)
        print()

    elif a == 'ucs':
        board = boards.InitialBoard(size=size, level=level)
        ff_problem = board.get_initial_board()
        print('UCS:')
        play_a_star_search(ff_problem, (null_heuristic, None))
        print()

    elif a == 'man':
        board = boards.InitialBoard(size=size, level=level)
        ff_problem = board.get_initial_board()
        print('A Star - Manhattan')
        play_a_star_search(ff_problem, (flow_free_heuristic, get_manhattan_distance))
        print()

    elif a == 'maze':
        board = boards.InitialBoard(size=size, level=level)
        ff_problem = board.get_initial_board()
        print('A Star - Maze')
        play_a_star_search(ff_problem, (flow_free_heuristic, get_maze_distance))
        print()


if __name__ == '__main__':
    main()
