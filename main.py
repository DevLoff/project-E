# IMPORT

from level_handler import *
from stage_handler import *

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
    gameStageTracker = [1] # 0:game ended, 1:game running, 2:level running, 3:peg launched
    eventList : list
    dt : float

    # MENU
    boxAspect = pygame.image.load("Images/no_tex.png").convert_alpha()
    buttons = [
        Button(pygame.Rect(100, 100, 100, 50), boxAspect, lambda x: narrow_visible(x, 1, 0, 2), True),
        Button(pygame.Rect(300, 100, 100, 50), boxAspect, lambda x: quit(), False),
        Button(pygame.Rect(500, 100, 100, 50), boxAspect, lambda x: launch_level(x,"level.pickle"), False),
    ]

    # GAME ELEMENTS
    level = Level()

    # VISUAL INITALISATION
    MENU_BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    MENU_BG.fill((255, 255, 255))
    menuDisplay = DisplayHandler(MENU_BG)
    STATIC_BG.blit(pygame.transform.scale(pygame.image.load("Images/bg_01_v01.png"),(SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))
    levelDisplay = DisplayHandler(STATIC_BG)

    menuDisplay.cover()

    # GAME LOOP
    while gameStageTracker[0]>0:
        # EVENT HANDLER
        dt = CLOCK.tick()/1000
        eventList = pygame.event.get()

        # TEMPORARY SYSTEM
        for evnt in eventList:
            if evnt.type == pygame.QUIT:
                gameStageTracker[0] = 0
            elif evnt.type == pygame.KEYDOWN:
                if evnt.key == pygame.K_ESCAPE:
                    if gameStageTracker[0] > 1:
                        gameStageTracker[0] = 1
                        menuDisplay.cover()
                    else:
                        gameStageTracker[0] = 0
            elif evnt.type == pygame.MOUSEBUTTONDOWN:
                if gameStageTracker[0]==2:
                    level.launch_peg()
                    gameStageTracker[0] = 3
                elif gameStageTracker[0]==1:
                    for button in buttons:
                        button.update(evnt.pos, buttons, gameStageTracker, levelDisplay, level)

        # PHYSIC
        if gameStageTracker[0]>2:
            gameStageTracker[0] = level.update(dt)
            if gameStageTracker[0] == 1:
                menuDisplay.cover()

        if gameStageTracker[0]>1:
            SCREEN.fill((0, 0, 0))
            levelDisplay.object_blit(level)
            levelDisplay.cycle()
        else:
            for button in buttons:
                menuDisplay.add_area(button.render(SCREEN))
            menuDisplay.cycle()

    quit()