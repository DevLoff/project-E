import pygame
from objects.input_obj import INPUTBOARD
from objects.game_obj import Game

if __name__ == '__main__':
    pygame.init()
    game = Game((800,600))

    INPUTBOARD.mod_input("launch", 0)
    INPUTBOARD.mod_input("reset", pygame.K_r)

    game.load_stage("stages/levels/level01.json")

    game.gameloop()

quit()