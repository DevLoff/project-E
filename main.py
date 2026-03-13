# IMPORT
import pygame
import math

"""
CONSTANT_CONSTANT : use upper case
variableVariable : use camel case
argumentargument : use lower case
function_function : use snake case
"""
def enlarge_range(origin,new):
    return [min(origin[0],new[0]),max(origin[1],new[1])]
def intersect(l1,l2):
    return (l1[0]<l2[1])==(l2[0]<l1[1])
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

def devmode(evnt,entry,toolkit):
    if len(pygame.key.name(evnt.key)) == 1:
        entry += pygame.key.name(evnt.key)
    if evnt.key == pygame.K_RETURN:
        if toolkit["state"] == "select" and entry.isdigit() and 0 <= int(entry) < len(level):
            toolkit["selected"] = level[int(entry)]
            toolkit["selected"].color = pygame.Color(255, 255, 0)
            toolkit["state"] = "edit"
            entry = ""
        if toolkit["state"] == "mode" and entry in toolkit["allowed"]:
            toolkit["state"] = entry
            entry = ""
        if toolkit["state"] == "edit":
            changes = entry.strip()
            if type(toolkit["selected"]) == ArcStatic and changes.count(';') == 2:
                dull = format_str_to_obj('a;' + changes)
                toolkit["selected"].update(dull.area, dull.startAngle, dull.endAngle)
            if type(toolkit["selected"]) == LineStatic and changes.count(';') == 1:
                dull = format_str_to_obj('l;' + changes)
                toolkit["selected"].update(dull.startPoint, dull.endPoint)
    if evnt.key == pygame.K_BACKSPACE:
        entry = entry[:-1]
    if evnt.key == pygame.K_ESCAPE:
        if toolkit["selected"] is not None:
            toolkit["selected"].color = pygame.Color(255, 255, 255)
        toolkit["state"] = "mode"
        entry = ""

    return entry


class ArcStatic:
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

class LineStatic:
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

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.circle(surface, (255,255,255), self.pos, self.radius)

    def static_collision_phy(self,dt,grav,res,fri,traces):
        prox = 100.0
        self.velocity += grav * dt
        self.velocity = self.velocity * res
        preshotPos = self.pos + self.velocity * dt
        for trace in traces:
            distance = trace.proximity(preshotPos)
            prox = min(prox,abs(distance))
            if abs(distance) < self.radius and trace.detection_area(preshotPos):
                self.velocity += trace.normal(self.velocity, self.pos) * (1 + self.bounciness)
                self.velocity = self.velocity * fri
        self.pos += self.velocity * dt
        return prox

if __name__ == '__main__':
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    GAMEFONT = pygame.font.SysFont("comicsansms",20)

    # VARIABLES
    isGameRunning = True
    isPhysicActive = False
    eventList : list
    rectClearanceList = []
    lateClearanceList = []
    inputString = ""
    dt : float
    editorDict = {
        "allowed": ["select"],
        "state":"mode",
        "selected":None,
    }

    # GAME ELEMENTS
    GRAVITY = pygame.Vector2(0,9.81) * 10
    AIRRESISTANCE = 1 - 0.00001
    GROUNDFRICTION = 1 - 0.0002
    THROWFORCE = 0.8

    level = level_read(open("level.txt","r").readlines())
    TEMPLATE = DiscBody(10,(SCREEN_WIDTH//2,0),(0,0),0.1)
    peg = TEMPLATE
    hydratation = [[0,0]]
    watering = []
    surf = 100.0
    SPLASH = 2.0

    # GAME LOOP
    while isGameRunning:
        # EVENT HANDLER
        dt = CLOCK.tick()/1000
        eventList = pygame.event.get()

        # TEMPORARY SYSTEM
        for evnt in eventList:
            if evnt.type == pygame.QUIT:
                isGameRunning = False
            elif evnt.type == pygame.KEYDOWN:
                inputString = devmode(evnt,inputString,editorDict)
            elif evnt.type == pygame.MOUSEBUTTONDOWN and not isPhysicActive:
                studiedPos = pygame.Vector2(evnt.pos)
                peg.velocity += (studiedPos - peg.pos) * THROWFORCE
                isPhysicActive = True

        # PHYSIC
        if isPhysicActive:
            surf = peg.static_collision_phy(dt,GRAVITY,AIRRESISTANCE,GROUNDFRICTION,level)
            if peg.pos.y > SCREEN_HEIGHT:
                isPhysicActive = False
                peg = TEMPLATE

        rectClearanceList.append(peg.render(SCREEN))
        for elt in level:
            rectClearanceList.append(elt.render(SCREEN))

        rectClearanceList.append(SCREEN.blit(GAMEFONT.render(editorDict["state"], True, (255, 255, 255)), (0, 0)))
        rectClearanceList.append(SCREEN.blit(GAMEFONT.render(inputString,True,(255,255,255)),(0,20)))
        rectClearanceList.append(SCREEN.blit(GAMEFONT.render(str(surf<12.0), True, (255, 255, 255)), (0, 40)))

        pygame.display.update(rectClearanceList+lateClearanceList)
        for rect in rectClearanceList:
            SCREEN.fill((0,0,0),rect)
        lateClearanceList = rectClearanceList.copy()
        rectClearanceList.clear()

    quit()