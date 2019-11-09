from random import randint
from BoardClasses import Move
from BoardClasses import Board

import math
# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.


class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2

        self.search_depth = 5

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]

        best_move = None
        best_move_score = -math.inf
        for outer_index in range(len(moves)):
            for inner_index in range(len(moves[outer_index])):
                self.board.make_move(
                    moves[outer_index][inner_index], self.color)
                move_score = self.search(
                    self.search_depth, moves[outer_index][inner_index], self.color, -math.inf, math.inf)
                self.board.undo()
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = moves[outer_index][inner_index]

        self.board.make_move(best_move, self.color)
        return best_move

    def search(self, depth, move, turn, alpha, beta):
        winner = self.board.is_win(turn)
        if winner != 0:
            if winner == -1:
                return 0
            if self.color == winner:
                return math.inf
            return -math.inf
        if depth == 0:
            score = self.board.black_count - self.board.white_count
            if self.color == 1:  # 1 = black
                return score
            return -score  # 2 = white

        if turn == self.color:  # min
            worst = math.inf
            possible_moves = self.board.get_all_possible_moves(
                self.opponent[self.color])
            for x in range(len(possible_moves)):
                for y in range(len(possible_moves[x])):
                    self.board.make_move(
                        possible_moves[x][y], self.opponent[self.color])
                    current = self.search(
                        depth-1, possible_moves[x][y], self.opponent[self.color], alpha, beta)
                    self.board.undo()
                    if current < worst:
                        worst = current
                    if current < beta:
                        beta = current
                    if beta <= alpha:
                        break
                else:
                    continue
                break
            return worst

        else:  # max
            best = -math.inf
            possible_moves = self.board.get_all_possible_moves(self.color)
            for x in range(len(possible_moves)):
                for y in range(len(possible_moves[x])):
                    self.board.make_move(possible_moves[x][y], self.color)
                    current = self.search(
                        depth-1, possible_moves[x][y], self.color, alpha, beta)
                    self.board.undo()
                    if current > best:
                        best = current
                    if current > alpha:
                        alpha = current
                    if beta <= alpha:
                        break
                else:
                    continue
                break
            return best
