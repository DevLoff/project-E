# IMPORT
import pygame

from physic_objs import *
from stage_handler import DisplayHandler
import pickle

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

if __name__ == '__main__':
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    STATIC_BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    GAMEFONT = pygame.font.SysFont("comicsansms",20)

    # META SETUP
    pygame.display.set_caption("Tears of Sky")
    pygame.display.set_icon(pygame.image.load("Images/logo.png"))

    # VARIABLES
    isGameRunning = True
    isLevelRunning = True
    isPhysicActive = False
    isPegLunched = False
    eventList : list
    inputString = ""
    dt : float

    # GAME ELEMENTS
    GRAVITY = pygame.Vector2(0,9.81) * 10
    AIRRESISTANCE = 1 - 0.00001
    THROWFORCE = 0.8

    ARCTP = lambda : ProtoArc((100,0),(0,0),(100,100))
    LINETP = lambda: ProtoLine( (0, 0), (100, 100))
    level = [
        ProtoArc((0,0),(800,0),(0,600))
    ]

    TEMPLATE = DiscBody(10,(SCREEN_WIDTH//2,0),(0,0),0)
    bench = [TEMPLATE.copy() for _ in range(5)]
    peg = bench.pop()
    distance = 100.0
    closestObj = None

    IMPACTSPLASH = 10
    fPos = -1
    lPos = -1
    surfTile = -1
    remTime = 0.0
    LINKTIME = 0.05

    TILESIZE = 50
    satTile = [0]*(SCREEN_WIDTH//TILESIZE)

    kickstartVel = pygame.Vector2(0,1)
    visualPos = TEMPLATE.pos.copy()
    visualVel = pygame.Vector2()

    # DEBUG MODE
    isDebugModeOn = True
    isDebugBGOn = False
    monitoredData = {
        "saturation":satTile,
        "tt water":0,
        "dist": 100,
        "tag": 0,
        "attempt left":len(bench),
    }
    isClicked = False
    a,b,c = 1,0,0
    select = 0

    # VISUAL INITALISATION
    STATIC_BG.blit(pygame.transform.scale(pygame.image.load("Images/bg_01_v01.png"),(SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))
    dHandler = DisplayHandler(STATIC_BG)

    # GAME LOOP
    while isGameRunning:
        # EVENT HANDLER
        dt = CLOCK.tick()/1000
        eventList = pygame.event.get()
        monitoredData["check"] = level[0].radius(natural_angle(peg.pos))

        # TEMPORARY SYSTEM
        for evnt in eventList:
            if evnt.type == pygame.QUIT:
                isGameRunning = False
            elif evnt.type == pygame.KEYDOWN:
                if evnt.key == pygame.K_ESCAPE:
                    isGameRunning = False
                elif evnt.key == pygame.K_SPACE:
                    isPhysicActive = not isPhysicActive
                elif evnt.key == pygame.K_F1:
                    isDebugModeOn = not isDebugModeOn
                elif evnt.key == pygame.K_F2 and isDebugModeOn:
                    isDebugBGOn = not isDebugBGOn
                elif evnt.key == pygame.K_F3 and isDebugModeOn:
                    isPegLunched = False
                    isPhysicActive = False
                    peg = TEMPLATE.copy()
                    isLevelRunning = True
                elif evnt.key == pygame.K_c and not isPegLunched and isLevelRunning:
                    peg.velocity += kickstartVel
                    isPegLunched = True
                    isPhysicActive = True
                elif evnt.key == pygame.K_w and isDebugModeOn:
                    level.append(ARCTP())
                elif evnt.key == pygame.K_x and isDebugModeOn:
                    level.append(LINETP())
                elif evnt.key == pygame.K_TAB and isDebugModeOn:
                    select = (select+1)%len(level)
                    a,b,c = 1,0,0

                elif evnt.key == pygame.K_a and isDebugModeOn:
                    a,b,c = 1,0,0
                elif evnt.key == pygame.K_z and isDebugModeOn:
                    a,b,c = 0,1,0
                elif evnt.key == pygame.K_e and isDebugModeOn:
                    a,b,c = 0,0,1

            elif evnt.type == pygame.MOUSEBUTTONDOWN:
                isClicked = True
            elif evnt.type == pygame.MOUSEBUTTONUP:
                isClicked = False
            elif evnt.type == pygame.MOUSEMOTION and isClicked:
                if type(level[select]) == ProtoArc:
                    level[select].update(level[select].vecCenter+pygame.Vector2(evnt.rel)*a,
                                level[select].startPoint+pygame.Vector2(evnt.rel)*b,
                                level[select].endPoint+pygame.Vector2(evnt.rel)*c)
                if type(level[select]) == ProtoLine:
                    level[select].update(level[select].startPoint+pygame.Vector2(evnt.rel)*a,
                                level[select].endPoint+pygame.Vector2(evnt.rel)*b)

        # PHYSIC
        if isPhysicActive:
            inContact,monitoredData["diff"],monitoredData["over"] = peg.static_collision_phy(dt,GRAVITY,AIRRESISTANCE,level)
            if 0.0 > peg.pos.y or  peg.pos.y > SCREEN_HEIGHT or 0.0 > peg.pos.x or peg.pos.x > SCREEN_WIDTH :
                if len(bench)>0:
                    isPegLunched = False
                    isPhysicActive = False
                    peg = bench.pop()
                    monitoredData["attempt left"] -= 1
                else:
                    isLevelRunning = False
                    isPegLunched = False
                    isPhysicActive = False
            if inContact:
                remTime = LINKTIME
            else:
                remTime = max(remTime-dt,-1)
            if remTime > 0.0:
                if fPos == -1:
                    fPos,lPos,surfTile = peg.pos.x,peg.pos.x,int(peg.pos.x // TILESIZE)
                else:
                    if int(peg.pos.x // TILESIZE) != surfTile:
                        satTile[int(peg.pos.x // TILESIZE)] += abs(lPos - fPos)
                        fPos, lPos, surfTile = peg.pos.x, peg.pos.x, int(peg.pos.x // TILESIZE)
                    else:
                        lPos = peg.pos.x
            elif lPos != -1:
                satTile[int(peg.pos.x // TILESIZE)] += abs(lPos - fPos)
                fPos, lPos, surfTile = -1,-1,-1

        monitoredData["tt water"] = sum(satTile)

        if not isPegLunched and isLevelRunning:
            kickstartVel = pygame.Vector2(pygame.mouse.get_pos()) - peg.pos
            visualPos = peg.pos.copy()
            visualVel = pygame.Vector2(kickstartVel)
            for i in range(4):
                visualVel += GRAVITY * 0.2
                visualVel *= AIRRESISTANCE
                visualPos += visualVel * 0.2
                dHandler.add_area(pygame.draw.circle(SCREEN,(255,255,255),visualPos,5))

        monitoredData["inside"] = level[select].detection_area(peg.pos)

        # DEBUG LAYER
        if isDebugModeOn:
            SCREEN.fill((0,0,0))
            align = 0
            for data in monitoredData:
                SCREEN.blit(GAMEFONT.render(f"{data} : {monitoredData[data]}",True,(255,255,255)),(0,20*align))
                align += 1
            for i in range(len(satTile)):
                tCol = ((int(peg.pos.x // TILESIZE) == i) * 125, (int(peg.pos.x // TILESIZE) == i) * 125,min(int(satTile[i]), 255))
                tPlace = pygame.Rect(TILESIZE * i, SCREEN_HEIGHT - TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(SCREEN, tCol, tPlace)
                SCREEN.blit(GAMEFONT.render(f"{satTile[i]}",True,(255,255,255)),(tPlace.topleft))
            peg.render(SCREEN)
            if type(level[select]) == ProtoArc:
                level[select].debug_render(SCREEN)
                pygame.draw.circle(SCREEN,(255,255,0),level[select].vecCenter*a+level[select].startPoint*b+level[select].endPoint*c,3)
            if type(level[select]) == ProtoLine:
                pygame.draw.circle(SCREEN,(255,255,0),level[select].startPoint*a+level[select].endPoint*b,3)
            pygame.draw.line(SCREEN,(255,0,0),peg.pos,peg.pos+peg.velocity)
            for elt in level:
                if elt == level[select]:
                    elt.render(SCREEN, (255, 255, 0))
                else:
                    elt.render(SCREEN,(255,255,255))
            pygame.display.flip()

        dHandler.cycle()

    quit()