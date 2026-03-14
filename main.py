# IMPORT
from physic_objs import *
from stage_handler import DisplayHandler

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


if __name__ == '__main__':
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    STATIC_BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    GAMEFONT = pygame.font.SysFont("comicsansms",20)

    # VARIABLES
    isGameRunning = True
    isPhysicActive = False
    isPegLunched = False
    eventList : list
    inputString = ""
    dt : float

    # GAME ELEMENTS
    GRAVITY = pygame.Vector2(0,9.81) * 10
    AIRRESISTANCE = 1 - 0.00001
    GROUNDFRICTION = 1 - 0.0002
    THROWFORCE = 0.8

    level = level_read(open("level.txt","r").readlines())
    TEMPLATE = DiscBody(10,(SCREEN_WIDTH//2,0),(0,0),0.1)
    peg = TEMPLATE.copy()
    distance = 100.0
    closestObj = None

    REACTION_RANGE = TEMPLATE.radius + 5
    IMPACTSPLASH = 10
    print(REACTION_RANGE)
    fPos = -1
    lPos = -1
    surfTile = -1

    TILESIZE = 50
    satTile = [0]*(SCREEN_WIDTH//TILESIZE)

    visualPos = TEMPLATE.pos.copy()
    visualVel = pygame.Vector2()

    # DEBUG MODE
    isDebugModeOn = True
    monitoredData = {
        "saturation":satTile,
        "dist": 0,
        "tag": 0
    }

    # VISUAL INITALISATION
    STATIC_BG.blit(pygame.transform.scale(pygame.image.load("Images/im.png"),(SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))
    dHandler = DisplayHandler(STATIC_BG)

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
                if evnt.key == pygame.K_SPACE:
                    isPhysicActive = not isPhysicActive
                if evnt.key == pygame.K_F6:
                    isDebugModeOn = not isDebugModeOn
            elif evnt.type == pygame.MOUSEBUTTONDOWN:
                if not isPegLunched:
                    studiedPos = pygame.Vector2(evnt.pos)
                    peg.velocity += (studiedPos - peg.pos) * THROWFORCE
                    isPegLunched = True
                    isPhysicActive = True

        # PHYSIC
        if isPhysicActive:
            distance,closestObj = peg.static_collision_phy(dt,GRAVITY,AIRRESISTANCE,GROUNDFRICTION,level)
            monitoredData["dist"],monitoredData["tag"] = distance,closestObj
            if peg.pos.y > SCREEN_HEIGHT:
                isPegLunched = False
                isPhysicActive = False
                peg = TEMPLATE.copy()
            if distance < REACTION_RANGE:
                if fPos == -1:
                    fPos,lPos,surfTile = peg.pos.x,peg.pos.x,int(peg.pos.x // TILESIZE)
                else:
                    if int(peg.pos.x // TILESIZE) != surfTile:
                        satTile[int(peg.pos.x // TILESIZE)] += max(IMPACTSPLASH, abs(lPos - fPos))
                        fPos, lPos, surfTile = peg.pos.x, peg.pos.x, int(peg.pos.x // TILESIZE)
                    else:
                        lPos = peg.pos.x
            elif lPos != -1:
                satTile[int(peg.pos.x // TILESIZE)] += max(IMPACTSPLASH,abs(lPos - fPos))
                fPos, lPos, surfTile = -1,-1,-1

        if not isPegLunched:
            visualPos = peg.pos.copy()
            visualVel = pygame.Vector2(pygame.mouse.get_pos()) - visualPos
            for i in range(4):
                visualVel += GRAVITY * 0.2
                visualVel *= AIRRESISTANCE
                visualPos += visualVel * 0.2
                dHandler.add_area(pygame.draw.circle(SCREEN,(255,255,255),visualPos,5))

        # DEBUG LAYER
        if isDebugModeOn:
            align = 0
            for data in monitoredData:
                dHandler.dynamic_blit(GAMEFONT.render(f"{data} : {monitoredData[data]}",True,(255,255,255)),(0,20*align))
                align += 1
            for i in range(len(satTile)):
                tCol = ((int(peg.pos.x // TILESIZE) == i) * 125, (int(peg.pos.x // TILESIZE) == i) * 125,min(int(satTile[i]), 255))
                tPlace = pygame.Rect(TILESIZE * i, SCREEN_HEIGHT - TILESIZE, TILESIZE, TILESIZE)
                dHandler.add_area(pygame.draw.rect(SCREEN, tCol, tPlace))
            dHandler.add_area(peg.render(SCREEN))
            for elt in level:
                dHandler.add_area(elt.render(SCREEN))

        dHandler.cycle()

    quit()