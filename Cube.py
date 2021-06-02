import random
import pygame as py


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


class Cube:
    def __init__(self, x, y, color):
        self.angle = 0
        self.speed = 9
        self.x = x
        self.y = y
        self.color = color
        self.rect = None
        self.width_and_length = 100
        self.num = random.randint(1, 6)

    def draw(self, screen):
        img = py.Surface((self.width_and_length, self.width_and_length))
        img.set_colorkey((0, 0, 0))
        img.fill(self.color)
        screen.blit(img, (self.x, self.y))
        self.draw_dots(screen, self.num)
        py.display.flip()

    def clicked_on(self, event):
        surface = py.Surface((self.width_and_length, self.width_and_length))
        self.rect = surface.get_rect()
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(py.mouse.get_pos())

    def draw_dots(self, screen, i):
        if i == 1:
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2, self.width_and_length / 2), 10, 0)
        if i == 2:
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2), 10, 0)
        if i == 3:
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2, self.width_and_length / 2), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 + 25), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 - 25), 10, 0)
        if i == 4:
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 + 20), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 + 20), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 - 20), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 - 20), 10, 0)
        if i == 5:
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2, self.width_and_length / 2), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 + 20), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 + 20), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 - 20), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 - 20), 10, 0)
        if i == 6:
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 + 30), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 - 25, self.width_and_length / 2 - 30), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 + 30), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2), 10, 0)
            py.draw.circle(screen, (0, 0, 255), (self.width_and_length / 2 + 25, self.width_and_length / 2 - 30), 10, 0)

    def roll(self, game, num):
        surface = py.Surface((self.width_and_length, self.width_and_length))
        self.rect = surface.get_rect()
        surface.set_colorkey((153, 76, 0))
        surface.fill(self.color)
        image = surface.copy()
        image.set_colorkey((153, 76, 0))
        rect = image.get_rect()
        rect.center = (self.width_and_length // 2, self.width_and_length // 2)
        clock = py.time.Clock()
        rot = 360
        running = True
        i = 0
        p = 0
        count = 0
        while running:
            clock.tick(60)
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
            py.draw.rect(game.screen, (153, 76, 0), (0, 0, 1700, 120))
            old_center = rect.center
            self.angle = (self.angle + self.speed) % rot
            new_image = py.transform.rotate(surface, self.angle)
            rect = new_image.get_rect()
            rect.center = old_center
            game.screen.blit(new_image, rect)
            self.draw_dots(game.screen, i)
            py.display.flip()
            if i == 6:
                i = 0
            if self.angle == 0:
                count += 1
            if p == 3:
                i += 1
                p = 0
            p += 1
            if count == 2:
                i = num
                rot = 90
            if count == 3:
                running = False
        self.speed = 9
        self.num = num
