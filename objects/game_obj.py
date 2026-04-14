import pygame
import json
from utils.stage_util import transform_raw
from objects.board_obj import INPUTBOARD

class Game:
    def __init__(self,size,save):
        self.size = pygame.Vector2(size)
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.stageId = None
        self.loadedStage = None
        self.current_stage = None
        self.loadingScreen = pygame.Surface(self.size)

        self.fpsave = save
        self.save = json.load(open(save,"r"))

        self.running = True

    def load_stage(self,filepath):
        self.window.blit(self.loadingScreen,(0,0))
        pygame.display.flip()
        self.stageId = filepath
        self.loadedStage = transform_raw(json.load(open(filepath, "r")))
        self.loadedStage.handling = self

    def add_data(self,tag,data):
        if self.stageId not in self.save:
            self.save[self.stageId] = dict()
        self.save[self.stageId][tag] = data

    def gameloop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            INPUTBOARD.update()

            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    self.running = False

            if self.loadedStage is not None:
                self.loadedStage.update(dt=dt)
                self.loadedStage.render()
        json.dump(self.save,open(self.fpsave,"w"))