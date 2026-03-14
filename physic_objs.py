from physic_utils import *

class StaticObj:
    def proximity(self, point) -> float:
        pass
    def detection_area(self, point) -> bool:
        pass
    def render(self, surface) -> pygame.Rect:
        pass

class ArcStatic(StaticObj):
    def __init__(self,rectangle,start_deg,end_deg) -> None:
        self.area = pygame.Rect(rectangle)
        self.color = pygame.Color(255,255,255)
        self.startAngle = start_deg
        self.endAngle = end_deg
        self.vecCenter = pygame.Vector2(self.area.center)
        self.halfsize = pygame.Vector2(self.area.size)/2
        self.startPoint = pygame.Vector2(round(self.halfsize.x*math.cos(start_deg),5),  round(self.halfsize.y*math.sin(start_deg),5)) + self.vecCenter
        self.endPoint = pygame.Vector2(round(self.halfsize.x*math.cos(end_deg),5),  round(self.halfsize.y*math.sin(end_deg),5)) + self.vecCenter
        self.radius = lambda alpha : round(math.sqrt((self.halfsize.x*math.cos(alpha))**2 + (self.halfsize.y*math.sin(alpha))**2),5)
        self.acute = abs(end_deg - start_deg) < math.pi
        self.startBracket = self.norm(self.startPoint).rotate(-90)
        self.endBracket = self.norm(self.endPoint).rotate(90)

    def norm(self,point) -> pygame.Vector2:
        trace = (self.vecCenter - point)
        if trace != pygame.Vector2():
            return trace.normalize()
        return trace

    def update(self,rectangle,start_deg,end_deg):
        self.area = pygame.Rect(rectangle)
        self.startAngle = start_deg
        self.endAngle = end_deg
        self.vecCenter = pygame.Vector2(self.area.center)
        self.halfsize = pygame.Vector2(self.area.size) / 2
        self.startPoint = pygame.Vector2(round(self.halfsize.x * math.cos(start_deg), 5),
                                         round(self.halfsize.y * math.sin(start_deg), 5)) + self.vecCenter
        self.endPoint = pygame.Vector2(round(self.halfsize.x * math.cos(end_deg), 5),
                                       round(self.halfsize.y * math.sin(end_deg), 5)) + self.vecCenter
        self.radius = lambda alpha: round(
            math.sqrt((self.halfsize.x * math.cos(alpha)) ** 2 + (self.halfsize.y * math.sin(alpha)) ** 2), 5)
        self.norm = lambda point: (self.vecCenter - point).normalize()
        self.acute = abs(end_deg-start_deg)<math.pi
        self.startBracket = self.norm(self.startPoint).rotate(-90)
        self.endBracket = self.norm(self.endPoint).rotate(90)

    def proximity(self, point) -> float:
        studiedPoint = pygame.Vector2(point)-self.vecCenter
        return self.radius(natural_angle(studiedPoint))-studiedPoint.length()

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return ((self.startBracket.dot(studiedPoint-self.startPoint)>0) + (self.endBracket.dot(studiedPoint-self.endPoint)>0)) >= 1 + self.acute

    def normal(self,vec,point=(0,0)) -> pygame.Vector2:
        studiedPoint = pygame.Vector2(point)
        return -vec.project(self.norm(studiedPoint))

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.arc(surface,self.color,self.area,-self.endAngle,-self.startAngle)

    def render_debug(self, surface) -> pygame.Rect:
        return pygame.draw.line(surface, (255, 255, 255), self.startPoint, self.endPoint)

class LineStatic(StaticObj):
    def __init__(self,start_point,end_point) -> None:
        self.color = pygame.Color(255,255,255)
        self.startPoint = pygame.Vector2(start_point)
        self.endPoint = pygame.Vector2(end_point)
        """
        lowcorner = pygame.Vector2(min(self.startPoint.x,self.endPoint.x),min(self.startPoint.y,self.endPoint.y))
        highcorner = pygame.Vector2(max(self.startPoint.x, self.endPoint.x), max(self.startPoint.y, self.endPoint.y))
        super().__init__(lowcorner,highcorner-lowcorner)
        """
        self.startBracket = (self.endPoint-self.startPoint).normalize()
        self.endBracket = (self.startPoint - self.endPoint).normalize()
        self.norm = self.startBracket.rotate_rad(math.pi/2)

    def update(self,start_point,end_point):
        self.startPoint = pygame.Vector2(start_point)
        self.endPoint = pygame.Vector2(end_point)
        self.startBracket = (self.endPoint - self.startPoint).normalize()
        self.endBracket = (self.startPoint - self.endPoint).normalize()
        self.norm = self.startBracket.rotate_rad(math.pi / 2)

    def proximity(self,point) -> float:
        studiedPoint = pygame.Vector2(point)-self.startPoint
        return self.norm.dot(studiedPoint)

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return self.startBracket.dot(studiedPoint - self.startPoint) > 0 and self.endBracket.dot(studiedPoint - self.endPoint) > 0

    def normal(self,vec,point=None) -> pygame.Vector2:
        return -vec.project(self.norm)

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.line(surface,self.color,self.startPoint,self.endPoint)

class DiscBody:
    def __init__(self,radius,initial_pos=(0,0),initial_vel=(0,0),bounce=0.0) -> None:
        self.radius = radius
        self.pos = pygame.Vector2(initial_pos)
        self.velocity = pygame.Vector2(initial_vel)
        self.bounciness = bounce

    def copy(self):
        return DiscBody(self.radius,self.pos.copy(),self.velocity.copy(),self.bounciness)

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.circle(surface, (255,255,255), self.pos, self.radius)

    def static_collision_phy(self,dt,grav,res,fri,traces):
        prox,close = 100.0,None
        self.velocity += grav * dt
        self.velocity = self.velocity * res
        preshotPos = self.pos + self.velocity * dt
        for trace in traces:
            distance = trace.proximity(preshotPos)
            if abs(distance) < self.radius and trace.detection_area(preshotPos):
                self.velocity += trace.normal(self.velocity, self.pos) * (1 + self.bounciness)
                self.velocity = self.velocity * fri
                prox = min(prox, abs(distance))
                if abs(distance) == prox:
                    close = traces.index(trace)
        self.pos += self.velocity * dt
        return prox,close