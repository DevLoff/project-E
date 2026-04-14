import pygame
import codecarbon
import time
from objects.board_obj import INPUTBOARD, SOUNDBOARD
from objects.game_obj import Game

if __name__ == '__main__':
    tracker = codecarbon.EmissionsTracker()
    tracker.start()
    startT = time.time()
    try :
        pygame.init()
        game = Game((800,600),"save.json")

        INPUTBOARD.mod_input("launch", 0)
        INPUTBOARD.mod_input("click", 0)
        INPUTBOARD.mod_input("reset", pygame.K_r)
        INPUTBOARD.mod_input("debug", pygame.K_d)

        SOUNDBOARD.mod_sound("click","Sound/clicksound1.mp3")

        game.load_stage("stages/menus/menu01.json")

        game.gameloop()
    finally:
        endT = time.time()
        print(tracker.stop()*50,"g equivalent in CO2 for your session")

quit()