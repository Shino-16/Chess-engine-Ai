import copy, random, numpy

class Heuristics:
    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

class AI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate_board(self, board):
        score = 0
        piece_value = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 1000
        }
        tables = {
            'pawn': Heuristics.PAWN_TABLE,
            'knight': Heuristics.KNIGHT_TABLE,
            'bishop': Heuristics.BISHOP_TABLE,
            'rook': Heuristics.ROOK_TABLE,
            'queen': Heuristics.QUEEN_TABLE
        }
        for row_idx, row in enumerate(board.squares):
            for col_idx, square in enumerate(row):
                if square.piece:
                    name = square.piece.name
                    value = piece_value[name]
                    if square.piece.color == 'white':
                        score += value
                        if square.piece.name in tables:
                            score += tables[name][row_idx][col_idx] / 100.0
                    else:
                        score -= value
                        if square.piece.name in tables:
                            score -= tables[name][7-row_idx][col_idx] / 100.0
        return score

    def get_all_legal_moves(self, board, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col].piece
                if piece and piece.color == color:
                    board.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        # Only add moves that are legal (no forward pawn captures)
                        if piece.name == 'pawn':
                            if move.final.col == col and board.squares[move.final.row][move.final.col].has_piece():
                                continue
                        moves.append((piece, move, row, col))
        return moves

    def minimax(self, board, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_moves = []
        if maximizing_player:
            max_eval = float('-inf')
            for piece, move, row, col in self.get_all_legal_moves(board, 'white'):
                temp_board = board.clone()
                temp_piece = temp_board.squares[row][col].piece
                temp_board.move(temp_piece, move, testing=True)
                eval, _ = self.minimax(temp_board, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_moves = [(piece, move)]
                elif eval == max_eval:
                    best_moves.append((piece, move))
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if best_moves:
                return max_eval, random.choice(best_moves)
            else:
                return max_eval, None
        else:
            min_eval = float('inf')
            for piece, move, row, col in self.get_all_legal_moves(board, 'black'):
                temp_board = board.clone()
                temp_piece = temp_board.squares[row][col].piece
                temp_board.move(temp_piece, move, testing=True)
                eval, _ = self.minimax(temp_board, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_moves = [(piece, move)]
                elif eval == min_eval:
                    best_moves.append((piece, move))
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if best_moves:
                return min_eval, random.choice(best_moves)
            else:
                return min_eval, None

    def get_best_move(self, board, color):
        maximizing = color == 'white'
        _, move = self.minimax(board, self.depth, maximizing)
        return move
