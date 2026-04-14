import pygame
from objects.board_obj import INPUTBOARD, SOUNDBOARD
from objects.game_obj import Game

pygame.init()
game = Game((800,600),"save.json")

INPUTBOARD.mod_input("launch", 0)
INPUTBOARD.mod_input("click", 0)
INPUTBOARD.mod_input("reset", pygame.K_r)
INPUTBOARD.mod_input("debug", pygame.K_d)

SOUNDBOARD.mod_sound("click","Sound/clicksound1.mp3")

game.load_stage("stages/levels/level02.json")

game.gameloop()

quit()