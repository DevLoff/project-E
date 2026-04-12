import pygame
import json
from utils.stage_util import transform_raw
from objects.input_obj import INPUTBOARD

class Game:
    def __init__(self,size):
        SIZE = pygame.Vector2(size)
        self.window = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.loadedStage = None
        self.loadingScreen = pygame.Surface(SIZE)

        self.running = True

    def load_stage(self,filepath):
        self.window.blit(self.loadingScreen,(0,0))
        pygame.display.flip()
        self.loadedStage = transform_raw(json.load(open(filepath, "rb")))
        self.loadedStage.handling = self

    def gameloop(self):
        while self.running:
            dt = self.clock.tick() / 1000
            INPUTBOARD.update()

            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    quit()

            if self.loadedStage is not None:
                self.loadedStage.update(dt=dt)
                self.loadedStage.render()