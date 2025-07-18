import os

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)

    def copy(self):
        new_pawn = Pawn(self.color)
        new_pawn.moved = self.moved
        new_pawn.en_passant = self.en_passant
        return new_pawn

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

    def copy(self):
        new_knight = Knight(self.color)
        new_knight.moved = self.moved
        return new_knight

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

    def copy(self):
        new_bishop = Bishop(self.color)
        new_bishop.moved = self.moved
        return new_bishop

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def copy(self):
        new_rook = Rook(self.color)
        new_rook.moved = self.moved
        return new_rook

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def copy(self):
        new_queen = Queen(self.color)
        new_queen.moved = self.moved
        return new_queen

class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)

    def copy(self):
        new_king = King(self.color)
        new_king.moved = self.moved
        new_king.left_rook = self.left_rook
        new_king.right_rook = self.right_rook
        return new_king