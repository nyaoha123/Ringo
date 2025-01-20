import numpy as np
import time

# オセロのボードサイズ
BOARD_SIZE = 6
EMPTY, BLACK, WHITE = 0, 1, -1
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class RingoAI:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        mid = BOARD_SIZE // 2
        self.board[mid-1][mid-1], self.board[mid][mid] = WHITE, WHITE
        self.board[mid-1][mid], self.board[mid][mid-1] = BLACK, BLACK
        self.current_player = BLACK

    def is_valid_move(self, row, col, player):
        if self.board[row, col] != EMPTY:
            return False
        for dr, dc in DIRECTIONS:
            r, c, found = row + dr, col + dc, False
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == -player:
                found = True
                r += dr
                c += dc
            if found and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == player:
                return True
        return False

    def get_valid_moves(self, player):
        return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.is_valid_move(r, c, player)]

    def apply_move(self, row, col, player):
        self.board[row, col] = player
        for dr, dc in DIRECTIONS:
            r, c, to_flip = row + dr, col + dc, []
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == -player:
                to_flip.append((r, c))
                r += dr
                c += dc
            if to_flip and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == player:
                for flip_r, flip_c in to_flip:
                    self.board[flip_r, flip_c] = player

    def evaluate(self):
        return np.sum(self.board)

    def is_game_over(self):
        return not self.get_valid_moves(BLACK) and not self.get_valid_moves(WHITE)

    def minimax(self, depth, alpha, beta, maximizing_player, start_time, time_limit=55):
        if depth == 0 or self.is_game_over() or (time.time() - start_time > time_limit):
            return self.evaluate()
        
        moves = self.get_valid_moves(self.current_player)
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = Othello()
                new_board.board = np.copy(self.board)
                new_board.apply_move(*move, self.current_player)
                new_board.current_player = -self.current_player
                eval_score = new_board.minimax(depth-1, alpha, beta, False, start_time)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = Othello()
                new_board.board = np.copy(self.board)
                new_board.apply_move(*move, self.current_player)
                new_board.current_player = -self.current_player
                eval_score = new_board.minimax(depth-1, alpha, beta, True, start_time)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self, max_depth=5):
        best_score = float('-inf')
        best_move = None
        start_time = time.time()
        
        for move in self.get_valid_moves(self.current_player):
            new_board = Othello()
            new_board.board = np.copy(self.board)
            new_board.apply_move(*move, self.current_player)
            new_board.current_player = -self.current_player
            score = new_board.minimax(max_depth, float('-inf'), float('inf'), False, start_time)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            if time.time() - start_time > 55:
                break
        
        return best_move

    def play_game(self):
        while not self.is_game_over():
            if self.current_player == BLACK:
                move = self.best_move()
                if move:
                    self.apply_move(*move, BLACK)
                self.current_player = WHITE
            else:
                move = self.best_move()
                if move:
                    self.apply_move(*move, WHITE)
                self.current_player = BLACK
            print(self.board)
        
        black_score = np.sum(self.board == BLACK)
        white_score = np.sum(self.board == WHITE)
        print(f"Final Score - BLACK: {black_score}, WHITE: {white_score}")
        if black_score > white_score:
            print("BLACK wins!")
        elif black_score < white_score:
            print("WHITE wins!")
        else:
            print("It's a draw!")

# ゲーム開始
game = Othello()
game.play_game()
