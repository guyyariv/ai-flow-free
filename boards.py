from flow_free_problems import FlowFreeProblem


class InitialBoard:

    def __init__(self, size=5, level='easy'):
        self.initial_board = self.generate_board(size, level)

    def get_initial_board(self):
        return self.initial_board

    def generate_board(self, size, level):
        if size == 5:
            ## level 14
            if level == 'easy':
                return FlowFreeProblem(5, 5, [[(3, 3), (4, 4)], [(0, 3), (4, 0)], [(2, 0), (0, 2)], [(0, 4), (3, 4)],
                                              [(4, 1), (2, 3)]])

            ## level 29
            if level == 'medium':
                return FlowFreeProblem(5, 5, [[(1, 1), (1, 3)], [(4, 0), (3, 4)], [(0, 0), (3, 4)], [(3, 0), (3, 4)],
                                              [(1, 0), (2, 3)]])

            ## level 15
            if level == 'hard':
                return FlowFreeProblem(5, 4, [[(4, 0), (2, 0)], [(0, 1), (4, 2)], [(4, 1), (1, 2)], [(0, 0), (2, 2)]])

        if size == 6:
            ## level 29
            if level == 'easy':
                return FlowFreeProblem(6, 6, [[(2, 0), (1, 1)], [(1, 2), (4, 1)], [(3, 0), (2, 3)], [(1, 0), (3, 5)],
                                              [(4, 5), (5, 3)], [(1, 3), (4, 4)]])

            ## level 15
            if level == 'medium':
                return FlowFreeProblem(6, 6, [[(0, 4), (3, 2)], [(0, 1), (5, 0)], [(0, 0), (4, 0)], [(5, 2), (0, 5)],
                                              [(0, 2), (2, 2)], [(1, 4), (4, 2)]])

            ## level 30
            if level == 'hard':
                return FlowFreeProblem(6, 6, [[(5, 0), (2, 0)], [(0, 0), (5, 3)], [(2, 3), (4, 4)], [(1, 0), (2, 1)],
                                              [(5, 1), (2, 4)], [(5, 2), (4, 3)]])

        if size == 7:
            ## level 17
            if level == 'easy':
                return FlowFreeProblem(7, 7, [[(0, 6), (4, 5)], [(3, 2), (5, 5)], [(5, 6), (5, 1)], [(2, 1), (3, 4)],
                                              [(4, 1), (6, 2)], [(3, 1), (3, 5)], [(1, 1), (2, 4)]])
            ## level 22
            if level == 'medium':
                return FlowFreeProblem(7, 7, [[(0, 0), (1, 3)], [(5, 2), (5, 5)], [(0, 2), (1, 2)], [(1, 4), (3, 2)],
                                              [(5, 1), (4, 5)], [(4, 6), (6, 0)], [(5, 0), (1, 5)]])
            if level == 'hard':
                return FlowFreeProblem(7, 7, [[(4, 1), (5, 5)], [(1, 0), (4, 2)], [(0, 5), (3, 6)], [(0, 2), (0, 4)],
                                              [(1, 5), (3, 4)], [(0, 0), (4, 0)], [(1, 2), (2, 4)]])
