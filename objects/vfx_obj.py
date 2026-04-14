import pygame
import random

from utils.image_util import handle_imglike


class Particle:
    def __init__(self, rect, img, density):
        area = pygame.Rect(rect)
        self.particle = handle_imglike(img)
        self.mouvement = pygame.Vector2()
        size = self.particle.get_size()
        n = round(density*area.w*area.h)
        poses = [
            pygame.Vector2(random.randint(0,area.w-size[0]), random.randint(0,area.h-size[1])) for _ in range(n)
        ]
        self.pos = pygame.Vector2(area.topleft)
        self.img = pygame.Surface(area.size,flags=pygame.SRCALPHA)
        for p in poses:
            self.img.blit(self.particle,p)

    def update(self,dt,grav):
        self.mouvement += dt*grav
        self.pos += self.mouvement*dt
        return self.pos.y