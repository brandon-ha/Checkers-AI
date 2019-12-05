from random import randint
from BoardClasses import Move
from BoardClasses import Board

import math
import time
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

        self.search_depth = 6
        self.debug = True
        self.time_used = 0

    def get_move(self, move):
        if self.debug:
            current_move_elapsed = time.time()

        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]

        how_many_moves = 0
        for outer_index in range(len(moves)):
            how_many_moves += len(moves[outer_index])

        depth = round((4/how_many_moves) + self.search_depth)

        if self.debug:
            print(how_many_moves, "possible moves")
            print("Depth:", depth)

        best_move = None
        best_move_score = -math.inf
        for outer_index in range(len(moves)):
            for inner_index in range(len(moves[outer_index])):
                self.board.make_move(moves[outer_index][inner_index], self.color)
                move_score = self.search(depth, moves[outer_index][inner_index], self.color, -math.inf, math.inf)
                self.board.undo()
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = moves[outer_index][inner_index]

        self.board.make_move(best_move, self.color)

        if self.debug:
            self.time_used += (time.time() - current_move_elapsed)
            print("Total elapsed time (in seconds):", self.time_used)

        return best_move

    def search(self, depth, move, turn, alpha, beta):
        winner = self.board.is_win(turn)
        win_return = 1000 + depth
        if winner != 0:
            if winner == -1:
                return 0
            if self.color == winner:
                return win_return
            return -win_return
        if depth == 0:
            black = 0
            white = 0
            for x in range(self.board.row):
                for y in range(self.board.col):
                    if self.board.board[x][y].color=="W":
                        white += 5
                        if self.board.board[x][y].is_king:
                            white += self.row + 2
                        else:
                            white += x

                    if self.board.board[x][y].color=="B":
                        black += 5
                        if self.board.board[x][y].is_king:
                            black += self.row + 2
                        else:
                            black += (self.row - x - 1)

            score = black - white
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