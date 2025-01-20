import random

BLACK = 1
WHITE = 2
CORNERS = [(0, 0), (0, 5), (5, 0), (5, 5)]

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True
    return False

def valid_moves(board, stone):
    return [(x, y) for y in range(len(board)) for x in range(len(board[0])) if can_place_x_y(board, stone, x, y)]

def score_move(board, x, y, stone):
    score = 0
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flipped = 0
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            flipped += 1
        if flipped > 0 and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            score += flipped
    return score

def evaluate_board(board, stone):
    opponent = 3 - stone
    score = 0

    # コーナー評価（非常に重要）
    for x, y in CORNERS:
        if board[y][x] == stone:
            score += 20
        elif board[y][x] == opponent:
            score -= 20

    # エッジ評価（重要だがコーナーほどではない）
    edges = [
        (0, 1), (0, 4), (1, 0), (1, 5),
        (4, 0), (4, 5), (5, 1), (5, 4)
    ]
    for x, y in edges:
        if board[y][x] == stone:
            score += 5
        elif board[y][x] == opponent:
            score -= 5

    # 石の総数（終盤に効果的）
    stone_count = sum(row.count(stone) for row in board)
    opponent_count = sum(row.count(opponent) for row in board)
    score += stone_count - opponent_count

    return score

def minimax(board, depth, maximizing_player, stone, alpha, beta):
    if depth == 0 or not valid_moves(board, stone):
        return evaluate_board(board, stone)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            new_board[y][x] = stone
            eval = minimax(new_board, depth - 1, False, 3 - stone, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            new_board[y][x] = stone
            eval = minimax(new_board, depth - 1, True, 3 - stone, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

class RingoAI:
    def face(self):
        return "🦾"

    def place(self, board, stone):
        best_move = None
        best_value = float('-inf')

        # ミニマックスの探索深さを4に増加
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            new_board[y][x] = stone
            move_value = minimax(new_board, 4, False, stone, float('-inf'), float('inf'))
            if move_value > best_value:
                best_value = move_value
                best_move = move
                
        return best_move

