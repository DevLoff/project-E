import pygame

from objects.physic_obj import DiscBody
from utils.image_util import handle_imglike

class UIItem:
    def __init__(self,rect,img):
        self.rect = pygame.Rect(rect)
        self.img = pygame.transform.scale(handle_imglike(img),self.rect.size)

class Peg(DiscBody):
    def __init__(self,radius,fp):
        super().__init__(radius)
        self.img = handle_imglike(fp)
        self.offset = - pygame.Vector2(self.img.get_rect().center)

class Port:
    def __init__(self,pos,fp):
        self.pos = pygame.Vector2(pos)
        self.img = handle_imglike(fp)
        self.offset = - pygame.Vector2(self.img.get_rect().center)

class Cloud:
    def __init__(self,pos,fp):
        self.pos = pygame.Vector2(pos)
        self.img = handle_imglike(fp)
        self.offset = - pygame.Vector2(self.img.get_rect().center)

        self.hitboxes = []

    def add_hitbox(self,static):
        static.move(self.pos)
        self.hitboxes.append(static)

class Field:
    def __init__(self,pos,fp):
        self.pos = pygame.Vector2(pos)
        self.img = handle_imglike(fp)
        self.offset = - pygame.Vector2(self.img.get_rect().center)
        self.range = self.pos.x + self.offset.x, self.pos.x - self.offset.x
        self.score = 0

    def update(self,peg):
        if self.range[0] <= peg.pos.x <= self.range[1]:
            self.score += peg.velocity.length()