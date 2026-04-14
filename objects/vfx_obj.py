import pygame
import random

class Droplet:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.speed = random.uniform(7, 12)
        self.length = random.randint(4, 8)
        self.active = True

    def update(self):
        self.pos[1] += self.speed
        if self.pos[1] > 580:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.line(screen, (160, 210, 255), (self.pos[0], self.pos[1]),
                             (self.pos[0], self.pos[1] + self.length), 1)
            pygame.draw.line(screen, (200, 240, 255), (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1] + 2), 1)