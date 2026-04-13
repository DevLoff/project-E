import pygame
import codecarbon
from objects.board_obj import INPUTBOARD, SOUNDBOARD
from objects.game_obj import Game

if __name__ == '__main__':
    tracker = codecarbon.EmissionsTracker()
    tracker.start()
    try :
        pygame.init()
        game = Game((800,600),"save.json")

        INPUTBOARD.mod_input("launch", 0)
        INPUTBOARD.mod_input("click", 0)
        INPUTBOARD.mod_input("reset", pygame.K_r)

        SOUNDBOARD.mod_sound("click","Sound/clicksound1.mp3")

        game.load_stage("stages/menus/menu01.json")

        game.gameloop()
    finally:
        tracker.stop()

quit()