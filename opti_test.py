import pygame
from objects.input_obj import INPUTBOARD
from objects.game_obj import Game
from utils.image_util import handle_imglike

if __name__ == '__main__':
    pygame.init()
    game = Game((800,600))

    INPUTBOARD.mod_input("launch", 0)
    INPUTBOARD.mod_input("click", 0)
    INPUTBOARD.mod_input("reset", pygame.K_r)

    game.load_stage("stages/menus/menu01.json")

    game.gameloop()

quit()