import pygame
import os


def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = pygame.image.load(folder + "/" + filename)
        if img is not None:
            images.append(img)
    return images


class Player:
    def __init__(self, surface, rect, gravity, image_path, walk_anim_path):
        self.surface = surface
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.gravity = gravity
        self.idle = pygame.image.load(image_path)
        self.idle = pygame.transform.scale(self.idle, (self.w, self.h))
        self.onFloor = True

        self.walk_cycle = load_images(walk_anim_path)
        for i in range(len(self.walk_cycle)):
            self.walk_cycle[i] = pygame.transform.scale(self.walk_cycle[i], (self.w, self.h))

        self.walk_cycle_state = 0
        self.walk_cycle_tick = 0

        self.velocity = [0, 0]

    def setVel(self, v):
        self.velocity = v

    def changeVel(self, v):
        self.velocity[0] += v[0]
        self.velocity[1] += v[1]

    def changeCoord(self, c):
        self.x += c[0]
        self.y += c[1]

    def move(self, timeElapsed):
        self.x += self.velocity[0] * timeElapsed
        self.y += self.velocity[1] * timeElapsed
        self.velocity[1] += self.gravity * timeElapsed

    def draw(self):
        if self.velocity[0] != 0:
            if self.velocity[0] > 0:
                self.surface.blit(self.walk_cycle[self.walk_cycle_state], (self.x, self.y))
            if self.velocity[0] < 0:
                self.surface.blit(self.walk_cycle[self.walk_cycle_state+3], (self.x, self.y))
            if self.walk_cycle_tick == 15:
                if self.walk_cycle_state < 2:
                    self.walk_cycle_state += 1
                else:
                    self.walk_cycle_state = 0
                self.walk_cycle_tick = 0
            else:
                self.walk_cycle_tick += 1
            return
        self.surface.blit(self.idle, (self.x, self.y))
