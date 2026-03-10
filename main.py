# IMPORT
import pygame
import math

"""
CONSTANT_CONSTANT : use upper case
variableVariable : use camel case
argumentargument : use lower case
function_function : use snake case
"""
def deg_to_rad(t):
    return t*math.pi/180
def natural_angle(vec):
    return deg_to_rad(pygame.Vector2(1,0).angle_to(vec))
def dipoint_arc_interpretation(curvature,p1,p2):
    fp1,fp2 = pygame.Vector2(p1),pygame.Vector2(p2)
    center = fp2+(fp1-fp2)/2 + (fp1-fp2).normalize().rotate(90) * (1/curvature)
    rectRad = pygame.Vector2(1,1) * (center-fp1).length()
    return ArcStatic(pygame.Rect(center-rectRad,rectRad*2),natural_angle(fp1-center),natural_angle(fp2-center))

def format_str_to_obj(elements):
    if elements[0]=='a':
        frect = [float(n) for n in elements[1].split(',')]
        a1,a2 = deg_to_rad(float(elements[2])),deg_to_rad(float(elements[3]))
        return ArcStatic(frect,a1,a2)
    if elements[0]=='t':
        curve,pts = float(elements[1]),[[float(n) for n in elements[i+2].split(',')] for i in range(2)]
        return dipoint_arc_interpretation(curve,pts[0],pts[1])
    if elements[0]=='l':
        p1,p2 = [float(n) for n in elements[1].split(',')],[float(n) for n in elements[2].split(',')]
        return LineStatic(p1,p2)
    return None
def level_read(data):
    return [format_str_to_obj(line.strip().split(';')) for line in data]


class ArcStatic(pygame.Rect):
    def __init__(self,rect,start_deg,end_deg) -> None:
        super().__init__(pygame.Rect(rect))
        self.startAngle = start_deg
        self.endAngle = end_deg
        self.vecCenter = pygame.Vector2(self.center)
        self.halfsize = pygame.Vector2(self.size)/2
        self.startPoint = pygame.Vector2(round(self.halfsize.x*math.cos(start_deg),5),  round(self.halfsize.y*math.sin(start_deg),5)) + self.vecCenter
        self.endPoint = pygame.Vector2(round(self.halfsize.x*math.cos(end_deg),5),  round(self.halfsize.y*math.sin(end_deg),5)) + self.vecCenter
        self.radius = lambda alpha : round(math.sqrt((self.halfsize.x*math.cos(alpha))**2 + (self.halfsize.y*math.sin(alpha))**2),5)
        self.norm = lambda point : (self.vecCenter - point).normalize()
        self.startBracket = self.norm(self.startPoint).rotate(-90)
        self.endBracket = self.norm(self.endPoint).rotate(90)

    def proximity(self, point) -> float:
        studiedPoint = pygame.Vector2(point)-self.vecCenter
        return self.radius(natural_angle(studiedPoint))-studiedPoint.length()

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return self.startBracket.dot(studiedPoint-self.startPoint)>0 and self.endBracket.dot(studiedPoint-self.endPoint)>0

    def normal(self,vec,point=(0,0)) -> pygame.Vector2:
        studiedPoint = pygame.Vector2(point)
        return -vec.project(self.norm(studiedPoint))

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.arc(surface,(255,255,255),self,-self.endAngle,-self.startAngle)

    def render_debug(self, surface) -> pygame.Rect:
        return pygame.draw.line(surface, (255, 255, 255), self.startPoint, self.endPoint)

class LineStatic(pygame.Rect):
    def __init__(self,start_point,end_point) -> None:
        self.startPoint = pygame.Vector2(start_point)
        self.endPoint = pygame.Vector2(end_point)
        lowcorner = pygame.Vector2(min(self.startPoint.x,self.endPoint.x),min(self.startPoint.y,self.endPoint.y))
        highcorner = pygame.Vector2(max(self.startPoint.x, self.endPoint.x), max(self.startPoint.y, self.endPoint.y))
        super().__init__(lowcorner,highcorner-lowcorner)
        self.startBracket = (self.endPoint-self.startPoint).normalize()
        self.endBracket = (self.startPoint - self.endPoint).normalize()
        self.norm = self.startBracket.rotate_rad(math.pi/2)

    def proximity(self,point) -> float:
        studiedPoint = pygame.Vector2(point)-self.startPoint
        return self.norm.dot(studiedPoint)

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return self.startBracket.dot(studiedPoint - self.startPoint) > 0 and self.endBracket.dot(studiedPoint - self.endPoint) > 0

    def normal(self,vec,point=None) -> pygame.Vector2:
        return -vec.project(self.norm)

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.line(surface,(255,255,255),self.startPoint,self.endPoint)

class DiscBody:
    def __init__(self,radius,initial_pos=(0,0),initial_vel=(0,0)) -> None:
        self.radius = radius
        self.pos = pygame.Vector2(initial_pos)
        self.velocity = pygame.Vector2(initial_vel)

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.circle(surface, (255,255,255), self.pos, self.radius)

    def static_collision_phy(self,dt,grav,res,fri,traces) -> None:
        self.velocity += grav * dt
        self.velocity = self.velocity * res
        preshotPos = peg.pos + self.velocity * dt
        for trace in traces:
            distance = trace.proximity(preshotPos)
            if abs(distance) < self.radius and trace.detection_area(preshotPos):
                self.velocity += trace.normal(self.velocity, preshotPos)
                self.velocity = self.velocity * fri
        self.pos += self.velocity * dt

if __name__ == '__main__':
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()

    # VARIABLES
    isGameRunning = True
    isPhysicActive = True
    eventList : list
    rectClearanceList = []
    lateClearanceList = []
    dt : float

    # GAME ELEMENTS
    GRAVITY = pygame.Vector2(0,9.81) * 10
    AIRRESISTANCE = 1 - 0.00001
    GROUNDFRICTION = 1 - 0.0002

    level = level_read(open("level.txt","r").readlines())
    peg = DiscBody(10,(50,0))

    # GAME LOOP
    while isGameRunning:
        # EVENT HANDLER
        dt = CLOCK.tick()/1000
        eventList = pygame.event.get()

        # TEMPORARY SYSTEM
        for evnt in eventList:
            if evnt.type == pygame.QUIT:
                isGameRunning = False
            if evnt.type == pygame.KEYDOWN:
                if evnt.key == pygame.K_SPACE:
                    isPhysicActive = not isPhysicActive

        # PHYSIC
        if isPhysicActive:
            peg.static_collision_phy(dt,GRAVITY,AIRRESISTANCE,GROUNDFRICTION,level)

        rectClearanceList.append(peg.render(SCREEN))
        for elt in level:
            rectClearanceList.append(elt.render(SCREEN))

        pygame.display.update(rectClearanceList+lateClearanceList)
        for rect in rectClearanceList:
            SCREEN.fill((0,0,0),rect)
        lateClearanceList = rectClearanceList.copy()
        rectClearanceList.clear()

    quit()