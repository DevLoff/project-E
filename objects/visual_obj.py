import pygame

from objects.physic_obj import DiscBody
from utils.image_util import handle_imglike

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
    def __init__(self,pos,fp,*statics):
        self.pos = pygame.Vector2(pos)
        self.img = handle_imglike(fp)
        self.offset = - pygame.Vector2(self.img.get_rect().center)

        self.hitboxes = []
        for static in statics:
            static.move(self.pos)
            self.hitboxes.append(static)