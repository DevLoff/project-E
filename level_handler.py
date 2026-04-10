import pygame.display

from physic_objs import *

class Peg:
    def __init__(self,rad,aspect):
        self.body = DiscBody(rad)
        self.aspect = aspect
        self.offset = pygame.Vector2(aspect.get_size())/2
    def render(self,surface):
        return surface.blit(self.aspect,self.body.pos-self.offset)


class Level:
    def __init__(self):
        self.platforms = []
        self.bench = []
        self.peg = None

        self.gravity = pygame.Vector2(0,9.81) * 10
        self.airres = 1 - 0.00001
        self.throw = 0.8

    def rack_peg(self):
        if len(self.bench)>0:
            self.peg = self.bench.pop()
            self.peg.body.pos = pygame.Vector2(400, 30)
            return 2
        return 1
    def launch_peg(self):
        if self.peg is not None:
            modality = self.get_launch_parameter()
            self.peg.body.velocity += modality[0]*modality[1]*self.throw
    def get_launch_parameter(self):
        inputVec = pygame.Vector2(pygame.mouse.get_pos()) - self.peg.body.pos
        return min(inputVec.length(),100),inputVec.normalize()

    def update(self,dt):
        self.peg.body.static_collision_phy(dt,self.gravity,self.airres,self.platforms)
        if not pygame.display.get_surface().get_rect().collidepoint(self.peg.body.pos):
            return self.rack_peg()
        return 3

    def render(self,surface):
        rectSet = []
        for platform in self.platforms:
            rectSet.append(platform.render(surface)[0])
        for sitting in self.bench:
            rectSet.append(sitting.render(surface))
        if self.peg is not None:
            rectSet.append(self.peg.render(surface))
        return rectSet