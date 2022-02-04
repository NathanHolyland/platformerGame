import pygame


class Brick:
    def __init__(self, surface, rect, texture_path):
        self.surface = surface
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.w, self.h))

    def changeCoords(self, c):
        self.x += c[0]
        self.y += c[1]

    def draw(self):
        self.surface.blit(self.texture, (self.x, self.y))

