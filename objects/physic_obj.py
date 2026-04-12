import pygame
import math

"""
DISCBODY
Principal object acting as a moving disc, represent the peg
"""

class DiscBody:
    def __init__(self,radius,initial_pos=(0,0),initial_vel=(0,0),bounce=0.0) -> None:
        self.radius = radius
        self.pos = pygame.Vector2(initial_pos)
        self.velocity = pygame.Vector2(initial_vel)
        self.bounciness = math.sqrt(bounce)

    def copy(self):
        return DiscBody(self.radius,self.pos.copy(),self.velocity.copy(),self.bounciness)

    def move_and_slide(self,dt,gravity,colliders):
        self.velocity += gravity * dt
        self.pos += self.velocity * dt
        collided = False
        for collider in colliders:
            if self.adjust_collide(collider):
                collided = True
        return collided

    def adjust_collide(self,collider):
        dist = collider.proximity(self.pos) - self.radius
        if dist < 0.0 and collider.in_range(self.pos):
            adjustment = collider.normal(self.pos)
            self.velocity -= self.velocity.project(adjustment) * (1 + self.bounciness)
            self.pos += adjustment * abs(dist)
            return True
        return False

"""
STATICOBJ
General representation of non moving platform
"""

class StaticObj:
    def move(self,disp) -> None:
        pass
    def normal(self,angle) -> pygame.Vector2:
        pass
    def proximity(self, point) -> float:
        pass
    def in_range(self, point) -> bool:
        pass
    def hitbox(self,surface) -> None:
        pass

"""
ARC
StaticObj taking the form of an arc, using an ellipse as the base
"""

class Arc(StaticObj):
    def __init__(self,center,fvertex,svertex) -> None:
        super().__init__()
        #Center
        self.center = pygame.Vector2(center)
        #Vertex
        self.fVertex,self.sVertex = pygame.Vector2(fvertex),pygame.Vector2(svertex)
        if self.fVertex.length()>self.sVertex.length():
            self.maxVertex = self.fVertex
            self.minVertex = self.sVertex
        else:
            self.maxVertex = self.fVertex
            self.minVertex = self.sVertex
        #Focus points
        self.fociRel = self.maxVertex.normalize() * math.sqrt(max(self.maxVertex.length() ** 2 - self.minVertex.length() ** 2, 0))
        self.fFocus, self.sFocus = self.center + self.fociRel, self.center - self.fociRel
        #Brackets TODO


    def normal(self,point) -> pygame.Vector2:
        fnorm = pygame.Vector2(point) - self.fFocus
        snorm = pygame.Vector2(point) - self.sFocus
        return fnorm.lerp(snorm,0.5).normalize()

    def proximity(self, point) -> float:
        study = (pygame.Vector2(point)-self.fFocus).length() + (pygame.Vector2(point)-self.sFocus).length()
        return study - 2*self.maxVertex.length()

    def in_range(self, point) -> bool:
        return True

"""
LINE
StaticObj representing a line/segment, using a straight as a base
"""

class Line(StaticObj):
    def __init__(self,spoint,epoint) -> None:
        super().__init__()
        self.sPoint = pygame.Vector2(spoint)
        self.ePoint = pygame.Vector2(epoint)
        self.stretch = self.ePoint - self.sPoint
        self.sBracket = self.stretch.normalize()
        self.eBracket = - self.sBracket

    def move(self,disp) -> None:
        self.sPoint += pygame.Vector2(disp)
        self.ePoint += pygame.Vector2(disp)

    def normal(self,point) -> pygame.Vector2:
        study = pygame.Vector2(point) - self.sPoint
        return study.project(self.stretch.rotate(90)).normalize()

    def proximity(self,point) -> float:
        study = (pygame.Vector2(point)-self.sPoint).project(self.normal(point))
        return study.length()

    def in_range(self, point) -> bool:
        study = pygame.Vector2(point)
        return (study-self.sPoint).dot(self.sBracket) * (study-self.ePoint).dot(self.eBracket) >= 0.0

    def hitbox(self,surface) -> None:
        pygame.draw.line(surface,(255,0,0),self.sPoint,self.ePoint,1)

class Circle(StaticObj):
    def __init__(self,center,radius) -> None:
        super().__init__()
        self.center = pygame.Vector2(center)
        self.radius = radius

    def move(self,disp) -> None:
        self.center += pygame.Vector2(disp)

    def normal(self,point) -> pygame.Vector2:
        study = pygame.Vector2(point) - self.center
        return study.normalize()

    def proximity(self,point) -> float:
        study = (pygame.Vector2(point) - self.center).length()
        return study - self.radius

    def in_range(self, point) -> bool:
        return True

    def hitbox(self,surface) -> None:
        pygame.draw.circle(surface,(255,0,0),self.center,self.radius)