import pygame
import sys
from const import WIDTH, HEIGHT, SQSIZE

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Select Mode')
        self.font = pygame.font.SysFont(None, 50)

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)
        return rect

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            pvp_rect = self.draw_text("1. Player vs Player", WIDTH//2, HEIGHT//2 - 40)
            ai_rect = self.draw_text("2. Player vs AI", WIDTH//2, HEIGHT//2 + 40)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_rect.collidepoint(event.pos):
                        return 'pvp'
                    elif ai_rect.collidepoint(event.pos):
                        return 'ai'
