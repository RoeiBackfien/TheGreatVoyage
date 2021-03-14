import pygame
from pygame.locals import *


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (200, 150, 150)
        self.rect = Rect(x, y, 300, 100)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Choose", True, (0, 255, 255))
        screen.blit(text, (self.x + 60, self.y + 30))
        pygame.display.flip()

    def clickedOn(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                return True
