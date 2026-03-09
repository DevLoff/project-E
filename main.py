# IMPORT
import pygame

"""
CONSTANT_CONSTANT : use upper case
variableVariable : use camel case
argumentargument : use lower case
function_function : use snake case
"""

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
    PPM = 10 #pixel per meter
    GRAVITY = pygame.Vector2(0,9.81) * PPM
    AIRRESISTANCE = 0.99999
    CURVECENTER = pygame.Vector2(90,70)
    CURVERADIUS = 100
    CURVEBOUNCINESS = 0
    CURVEPOS = [CURVECENTER+CURVERADIUS*pygame.Vector2(1,0).rotate(180),CURVECENTER+CURVERADIUS*pygame.Vector2(1,0).rotate(60)]
    CURVESEG = [(CURVECENTER-CURVEPOS[0]).rotate(90),(CURVECENTER-CURVEPOS[1]).rotate(-90)]

    pegRadius = 5
    pegImg = pygame.Surface((10,10),pygame.SRCALPHA)
    pygame.draw.circle(pegImg,(255,0,0),(5,5),5)
    pegPos = pygame.Vector2(50,0)
    pegVelocity = pygame.Vector2(0,0)

    # ORIGIN ACTION
    pegVelocity += pygame.Vector2(0,0)

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
                    print(CURVEPOS)

        # PHYSIC
        if isPhysicActive:
            # NATURAL FORCES
            pegVelocity += GRAVITY*dt
            pegVelocity = pegVelocity * AIRRESISTANCE
            # COLLISION FORCES
            diff = CURVECENTER-(pegPos+pegVelocity*dt)
            distance = CURVERADIUS-diff.length()
            if abs(distance)<pegRadius and CURVESEG[0].dot(pegPos-CURVEPOS[0])>0 and CURVESEG[1].dot(pegPos-CURVEPOS[1])>0 :
                normal = diff.normalize().rotate(90)
                ratio = distance / pegVelocity.length()
                pegVelocity = normal*normal.dot(pegVelocity*ratio) + pegVelocity*(1-ratio)
            pegPos += pegVelocity*dt


        rectClearanceList.append(pygame.draw.circle(SCREEN,(0,255,0),CURVECENTER,CURVERADIUS))
        rectClearanceList.append(SCREEN.blit(pegImg,pegPos-pygame.Vector2(5,5)))
        rectClearanceList.append(pygame.draw.lines(SCREEN,(255,255,255),True,[CURVEPOS[0],CURVECENTER,CURVEPOS[1]],5))
        pygame.display.update(rectClearanceList+lateClearanceList)
        for rect in rectClearanceList:
            SCREEN.fill((0,0,0),rect)
        lateClearanceList = rectClearanceList.copy()
        rectClearanceList.clear()

    quit()