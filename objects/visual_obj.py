import pygame

from objects.physic_obj import DiscBody,Arc,Line
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
            if static[0] == 'a':
                self.hitboxes.append(Arc(
                    pygame.Vector2(static[1])+self.pos,
                    static[2],
                    static[3]
                ))
            if static[0] == 'l':
                self.hitboxes.append(Line(
                    pygame.Vector2(static[1]) + self.pos,
                    pygame.Vector2(static[2]) + self.pos
                ))