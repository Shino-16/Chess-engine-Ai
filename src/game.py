import pygame
import collections

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:

    def __init__(self, mode=None):
        self.mode = mode
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        # Pieces captured from white (shown near Player 2/Black)
        self.captured_white = []
        # Pieces captured from black (shown near Player 1/White)
        self.captured_black = []

    # blit methods

    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (X_OFFSET + col * SQSIZE, Y_OFFSET + row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (X_OFFSET - 25, Y_OFFSET + 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (X_OFFSET + col * SQSIZE + SQSIZE - 20, Y_OFFSET + HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = X_OFFSET + col * SQSIZE + SQSIZE // 2, Y_OFFSET + row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (X_OFFSET + move.final.col * SQSIZE, Y_OFFSET + move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (X_OFFSET + pos.col * SQSIZE, Y_OFFSET + pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (X_OFFSET + self.hovered_sqr.col * SQSIZE, Y_OFFSET + self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    def show_player_boxes(self, surface, mode):
        box_color = (40, 40, 40)
        border_color = (200, 200, 200)
        font = self.config.font

        # Player 1 box (bottom right)
        p1_rect = pygame.Rect(PLAYER1_BOX_X, PLAYER1_BOX_Y, PLAYER_BOX_WIDTH, PLAYER_BOX_HEIGHT)
        pygame.draw.rect(surface, box_color, p1_rect)
        pygame.draw.rect(surface, border_color, p1_rect, 2)
        p1_label = font.render("Player 1 (White)", True, (255, 255, 255))
        surface.blit(p1_label, p1_label.get_rect(center=p1_rect.center))

        # Player 2 or AI box (top right)
        p2_rect = pygame.Rect(PLAYER2_BOX_X, PLAYER2_BOX_Y, PLAYER_BOX_WIDTH, PLAYER_BOX_HEIGHT)
        pygame.draw.rect(surface, box_color, p2_rect)
        pygame.draw.rect(surface, border_color, p2_rect, 2)
        if mode == 'pvp':
            p2_text = "Player 2 (Black)"
        else:
            p2_text = "AI (Black)"
        p2_label = font.render(p2_text, True, (255, 255, 255))
        surface.blit(p2_label, p2_label.get_rect(center=p2_rect.center))

        # --- Captured pieces for Player 2 (Black) ---
        x = PLAYER2_BOX_X + 10
        y = PLAYER2_BOX_Y + PLAYER_BOX_HEIGHT + 10
        # Group by piece type
        counter = collections.Counter([piece.name for piece in self.captured_white])
        for piece_name, count in counter.items():
            # Find a piece object to get the texture
            piece_obj = next(p for p in self.captured_white if p.name == piece_name)
            img = pygame.image.load(piece_obj.texture)
            img = pygame.transform.scale(img, (32, 32))
            surface.blit(img, (x, y))
            if count > 1:
                font = self.config.font
                count_label = font.render(f"x{count}", True, (255, 255, 255))
                surface.blit(count_label, (x + 20, y + 16))
            x += 36

        # --- Captured pieces for Player 1 (White) ---
        x = PLAYER1_BOX_X + 10
        y = PLAYER1_BOX_Y - 42
        counter = collections.Counter([piece.name for piece in self.captured_black])
        for piece_name, count in counter.items():
            piece_obj = next(p for p in self.captured_black if p.name == piece_name)
            img = pygame.image.load(piece_obj.texture)
            img = pygame.transform.scale(img, (32, 32))
            surface.blit(img, (x, y))
            if count > 1:
                font = self.config.font
                count_label = font.render(f"x{count}", True, (255, 255, 255))
                surface.blit(count_label, (x + 20, y + 16))
            x += 36

    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()

    def capture_piece(self, captured_piece):
        if captured_piece:
            if captured_piece.color == 'white':
                self.captured_white.append(captured_piece)
            else:
                self.captured_black.append(captured_piece)

    def is_game_over(self):
        # Check if the current player has any valid moves
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if square.has_piece() and square.piece.color == self.next_player:
                    self.board.calc_moves(square.piece, row, col, bool=True)
                    if square.piece.moves:
                        return False
        return True