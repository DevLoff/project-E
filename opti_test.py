import pygame
from objects.level_obj import Level
from objects.visual_obj import Peg, Port, Cloud

if __name__ == '__main__':
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()

    # VARIABLES
    dt : float

    # GAME ELEMENTS
    currentLevel = Level()

    currentLevel.ports.append(
        Port((400,20),"Images/no_tex.png")
    )
    currentLevel.initialize_pegs(
        Peg(10,"Images/peg.png"),
        Peg(10, "Images/peg.png"),
        Peg(10, "Images/peg.png"),
    )
    currentLevel.initialize_cloud(
        Cloud((400,300),None,('a',(0,0),(50,0),(0,50))),
        #Cloud((400, 200), None, ('l', (-100, -100), (100, 100))),
    )


    currentLevel.arrange_bench((20,20),(40,0))
    currentLevel.set_staticlayers(
        pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    )

    # GAME LOOP
    while currentLevel.feasibility()>0:
        dt = CLOCK.tick()/1000

        # FORCE QUIT
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                quit()

        currentLevel.update(dt)
        currentLevel.render()

quit()