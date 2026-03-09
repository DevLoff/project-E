class Hitbox:
    def collidepoint(self,point) -> bool:
        pass

from pygame import Vector2

class NSideBox(Hitbox):
    def __init__(self,points:list) -> None:
        assert len(points)>1, "A NSideBox (polygone) needs at least two points"
        self.points = [Vector2(point) for point in points]
        self.edges = [self.points[i+1]-self.points[i] for i in range(len(self.points)-1)]
        self.edges.append(self.points[0]-self.points[-1])
        self.count = len(self.edges)

    def collidepoint(self,point) -> bool:
        study,count = Vector2(point),0
        for i in range(self.count):
            count+=int(study.dot(self.edges[i])>0)
        return not (count == self.count or count == 0)