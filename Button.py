import pygame
from pygame.locals import *


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.height = height
        self.color = color  # (200, 150, 150)
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(self.text, True, (0, 255, 255))
        screen.blit(text, (self.x + 60, self.y + 30))

    def clicked_on(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pygame.mouse.get_pos())
