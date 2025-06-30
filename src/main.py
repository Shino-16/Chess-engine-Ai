import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from menu import Menu
from ai import AI

class Main:

    def __init__(self):
        pygame.init()
        self.mode = Menu().run()  # Get game mode first
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game(self.mode)
        self.ai = AI(depth=2)  # AI player is always black (2)

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # Draw the right sidebar background in Dark Olive Green
            pygame.draw.rect(screen, (85, 107, 47), (800, 0, SIDEBAR_WIDTH, HEIGHT))

            # Draw player boxes and the rest
            game.show_player_boxes(screen, game.mode)
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    # Adjust for offsets
                    mx, my = event.pos
                    clicked_col = (mx - X_OFFSET) // SQSIZE
                    clicked_row = (my - Y_OFFSET) // SQSIZE

                    # Only proceed if inside the board
                    if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.next_player:
                                # When selecting a piece:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.show_player_boxes(screen, game.mode)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    motion_col = (mx - X_OFFSET) // SQSIZE
                    motion_row = (my - Y_OFFSET) // SQSIZE

                    # Only set hover if inside the board
                    if 0 <= motion_row < ROWS and 0 <= motion_col < COLS:
                        game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        game.show_player_boxes(screen, game.mode)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        mx, my = event.pos
                        released_col = (mx - X_OFFSET) // SQSIZE
                        released_row = (my - Y_OFFSET) // SQSIZE

                        if 0 <= released_row < ROWS and 0 <= released_col < COLS:
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            if board.valid_move(dragger.piece, move):
                                captured_piece = board.squares[released_row][released_col].piece
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)
                                board.set_true_en_passant(dragger.piece)
                                if captured:
                                    game.capture_piece(captured_piece)
                                game.play_sound(captured)
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                game.show_player_boxes(screen, game.mode)
                                game.next_turn()
                        dragger.undrag_piece()

                                # --- AI MOVE LOGIC ---
                        if game.mode == 'ai' and game.next_player == 'black':
                                    _, ai_move = self.ai.minimax(board, self.ai.depth, False)
                                    if ai_move:
                                        piece, move = ai_move
                                        if board.valid_move(piece, move):
                                            captured = board.squares[move.final.row][move.final.col].has_piece()
                                            if captured:
                                                captured_piece = board.squares[move.final.row][move.final.col].piece
                                            board.move(piece, move)
                                            board.set_true_en_passant(piece)
                                            if captured:
                                                game.capture_piece(captured_piece)
                                            game.play_sound(captured)
                                            game.show_bg(screen)
                                            game.show_last_move(screen)
                                            game.show_pieces(screen)
                                            game.show_player_boxes(screen, game.mode)
                                            game.next_turn()

                # key press and quit handling...
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.mainloop()
