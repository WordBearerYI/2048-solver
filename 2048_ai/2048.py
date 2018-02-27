import random
import copy


class MoveSimulator(object):
    def __init__(self, size=10):
        self.board = [None] * size

    def minimax(self, board, depth=1, max_move=True):

        legal_moves = self.get_moves(board)
        best_move = (float("inf"), (-1, -1))

        if depth == 0 or len(legal_moves) == 0:
            return (self.heuristic(board), (-1, -1))

        if max_move:
            best_move = (float("-inf"), (-1, -1))
            score = best_move[0]
            for m in legal_moves:
                result = self.minimax(self.forecast(m, board), depth - 1, not max_move)
                if result[0] > score:
                    best_move = (result[0], m)
                    score = result[0]

        else:
            best_move = (float("inf"), (-1, -1))
            score = best_move[0]
            for m in legal_moves:
                result = self.minimax(self.forecast(m, board), depth - 1, not max_move)
                if result[0] < score:
                    best_move = (result[0], m)
                    score = result[0]

        return best_move

    def alphabeta(self, board, depth=1, alpha=float("-inf"), beta=float("inf"), max_move=True):

        legal_moves = self.get_moves(board)

        if depth == 0 or len(legal_moves) == 0:
            return (self.heuristic(board), (-1, -1))

        if max_move:
            best_move = (float("-inf"), (-1, -1))
            score = best_move[0]
            for move in legal_moves:
                result = self.alphabeta(self.forecast(move, board), depth - 1, alpha, beta, not max_move)
                if result[0] > score:
                    best_move = (result[0], move)
                    score = result[0]

                if result[0] >= beta:
                    return score, move

                alpha = max(alpha, result[0])

        else:
            best_move = (float("inf"), (-1, -1))
            score = best_move[0]
            for move in legal_moves:
                result = self.alphabeta(self.forecast(move, board), depth - 1, alpha, beta, not max_move)
                if result[0] < score:
                    best_move = (result[0], move)
                    score = result[0]

                if result[0] <= alpha:
                    return (result[0], move)

                beta = min(beta, result[0])

        return best_move

    def move(self, coordinates, position):
        """ Put a new move on the board and try calculate the next best move

            Parameters
            ----------
            coordinates : (1,1)
            position : (int)

            Returns
            -------
                The best coordinates for the next move

        """
        self.board.insert(position, coordinates)
        return self.minimax(self.board)[1]

    def forecast(self, coordinates, board):
        """ Put a new move in a copy of the current board

            Parameters
            ----------
            board : object
            coordinates : (1,1)

            Returns
            -------
            board
                The board with new move
        """
        new_board = copy.deepcopy(board)
        new_board.append(coordinates)
        return new_board

    def get_number_of_potential_moves(self, board):
        """Return size of potential moves

        Returns
        -------
        (int)
            size of potential moves
        """

        potential_moves = 0

        for a in board:
            if a == None:
                potential_moves += 1

        return potential_moves

    def get_moves(self, board):
        """Return pseudo random potential moves

        Returns
        -------
        list (int, int)
            size of potential moves
        """

        ms = []

        for a in range(self.get_number_of_potential_moves(board)):
            ms.append((random.randint(0, 9), random.randint(0, 9)))

        return ms

    def heuristic(self, board):
        """Calculate the heuristic value based in simple rules.

            Parameters
            ----------
            board : object

            Returns
            -------
            float
                The heuristic value of the current move of board
        """
        points = 0

        for coordinates in [i for i in board if i is not None]:

            if coordinates[0] > coordinates[1]:
                points += random.randint(20, 60)
            else:
                points += random.randint(0, 19)

        return points